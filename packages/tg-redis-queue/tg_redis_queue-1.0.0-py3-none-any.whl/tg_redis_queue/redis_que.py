import json
import logging
import time
import typing
import uuid
from dataclasses import dataclass, field

import redis


@dataclass
class RedisQueItem:
    """
    Representation of single queue item.

    :param data: queue item data, as dict that can be json-dumped
    :param key: identifier of item that is unique. Random is generated if not provided. Used to avoid
    adding duplicate entries to the queue.
    """

    data: dict
    key: str = field(default_factory=lambda: uuid.uuid4().hex)


class RedisObjectQueue:
    """Usage:

    >>> add = RedisObjectQueue(name='example_que')
    >>> add.add({'key': 1})
    >>> add.add({'key': 2})
    >>> add.add({'key': 3})
    >>> add.add({'key': 4})
    >>> add.add({'key': 5})

    >>> worker = RedisObjectQueue(name='example_que')
    >>> items = worker.get_items(end=3)
    >>> print(items)
    >>> [{'key': 1}, {'key': 2}, {'key': 3}]
    >>>
    >>> # Then: process the items
    >>>
    >>> # Finally remove the items from the que
    >>> print(worker.remove(items))
    >>> 3
    """

    # Implementation details:
    #
    # Uses redis sorted sets to store queue item order. Sorted sets are sets sorted by "score" which is provided
    # when item is added to set. Current time is used for score when adding item, so that items that are added
    # earlier come first in the queue.
    #
    # Uses redis hashes to store queue item values. Hashes are maps between the string fields and the string
    # values.
    #
    # Scores set is single source of truth about presence or absence of item in the queue (in case of race conditions)
    #
    # To reliably determine if queue is empty, use `get_total_size` and compare it to 0. `get()` and `pop()` may return
    # None for non-empty queue, due to race conditions between different workers

    # Expiry time in seconds, if None queue won't expire (and then you are responsible to clean it up)
    EXPIRY_TIME = 60

    def __init__(self, name: str, redis_url: typing.Optional[str] = None):
        self._name = name
        self.redis = redis.StrictRedis.from_url(redis_url or self._get_redis_url())

    def _get_redis_url(self):
        raise NotImplementedError(
            "Subclass RedisObjectQueue and override `_get_redis_url` or provide redis_url when creating the instance.",
        )

    def _get_scores_key(self) -> str:
        """Redis key for sorted set with the queue ordering scores"""
        return f"{self._name}:scores"

    def _get_values_key(self) -> str:
        """Redis key for hash with queue item values"""
        return f"{self._name}:values"

    def _update_expiry_time(self) -> None:
        if self.EXPIRY_TIME:
            self.redis.expire(self._get_values_key(), self.EXPIRY_TIME)
            self.redis.expire(self._get_scores_key(), self.EXPIRY_TIME)

    def get_expiry_time(self) -> typing.Optional[int]:
        expiry_time = self.redis.ttl(self._get_values_key())

        # -1 - never expires
        if expiry_time == -1:
            return None

        # -2 - does not exist, so practically expired (or not yet created)
        if expiry_time == -2:
            return 0 if self.EXPIRY_TIME is not None else None

        return expiry_time

    def add(self, data: typing.Union[RedisQueItem, dict]) -> None:
        """Add single item to the end of the queue"""
        if not isinstance(data, RedisQueItem):
            item = RedisQueItem(data)
        else:
            item = data

        logging.debug("Adding data to que %s: %r", self._name, item.data)

        # Adding to values first, so that in case of add/remove race every key has value
        # (keys are taken from scores set)

        # HSET sets a single key to value in the hash
        self.redis.hset(self._get_values_key(), key=item.key, value=json.dumps(item.data))

        # ZADD adds key-score pairs to sorted set (we only need to add one).
        # `nx=True` makes redis only add new items, without updating the score for existing ones
        # (so that if something is queued two times, the earliest place in the queue is kept by it)
        self.redis.zadd(self._get_scores_key(), {item.key: time.time()}, nx=True)
        self._update_expiry_time()

    def move_to_end(self, item: RedisQueItem) -> None:
        """Move an item to end of the queue, if it is still in the queue"""
        # `xx=True` makes redis only update existing items, so if item was already deleted it won't be moved
        self.redis.zadd(self._get_scores_key(), {item.key: time.time()}, xx=True)
        self._update_expiry_time()

    def get(self) -> typing.Optional[RedisQueItem]:
        """Get single item from the beginning of the queue, keeping it in the queue"""
        result = self.get_items(start=0, end=0)

        if result:
            return result[0]

        return None

    def pop(self) -> typing.Optional[RedisQueItem]:
        """Get single item from the beginning of the queue, removing it from the queue"""
        item = self.get()
        if not item:
            return None

        self.remove_item(item)
        return item

    def get_items(self, start: int = 0, end: int = 100) -> typing.List[RedisQueItem]:
        """Get multiple items from the queue.

        NB: number of items returned can be less than end-start even if the queue is full, if there is a race condition
        between reading the queue and deleting items from the queue
        """
        keys = self.redis.zrange(self._get_scores_key(), start, end)
        return self._handle_results(keys or [])

    def remove_item(self, item: RedisQueItem) -> bool:
        """Removes a queue item, returns true if item was found and deleted, false otherwise"""
        if not isinstance(item, RedisQueItem):
            raise TypeError(f"Expected RedisQueItem, found {type(item)}.")

        return bool(self.remove([item]))

    def prune(self) -> None:
        """Empties queue"""

        # Prune all items related to the queue
        self.redis.delete(
            self._get_values_key(),
            self._get_scores_key(),
        )

    def get_total_size(self) -> int:
        """Returns total size of the queue"""
        return self.redis.zcard(self._get_scores_key())

    def remove(self, data: typing.List[RedisQueItem]) -> int:
        """Removes the queue items, returns number of items removed."""
        if not isinstance(data, list):
            raise TypeError(f"Expected data to be a list, found {type(data)}.")

        keys_to_remove = []

        for item in data:
            if not isinstance(item, RedisQueItem):
                raise TypeError(f"Expected only RedisQueItem as data items, found {type(item)}.")

            keys_to_remove.append(item.key)

        scores_deleted: int = self.redis.zrem(self._get_scores_key(), *keys_to_remove)
        values_deleted: int = self.redis.hdel(self._get_values_key(), *keys_to_remove)

        if scores_deleted != values_deleted:
            logging.warning(
                "Deleted %d scores, but %d values, possible race condition.",
                scores_deleted,
                values_deleted,
            )

        return scores_deleted

    def _handle_results(self, keys: typing.List[str]) -> typing.List[RedisQueItem]:
        """Converts strings returned from redis to RedisQueItem instances"""
        if not keys:
            return []

        result = []
        for key in keys:
            key_string = key.decode("utf-8")
            value = self.redis.hget(self._get_values_key(), key_string)
            # It is possible that due to read/delete race, the value is already gone - then, skip it
            if value:
                value_string = value.decode("utf-8")
                result.append(RedisQueItem(json.loads(value_string), key=key_string))

        return result
