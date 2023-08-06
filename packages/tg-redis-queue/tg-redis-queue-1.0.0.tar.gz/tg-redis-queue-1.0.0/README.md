# Thorgate :: Redis Queue

Redis queue, that can be easily used to store json-compatible dictionaries and is aimed to be race-condition proof.

## Example usage

```python
from tg_redis_queue import RedisObjectQueue


class MyRedisObjectQueue(RedisObjectQueue):
    def _get_redis_url(self):
        # Can alternatively use base RedisObjectQueue and provide 
        # redis_url to constructor, like 
        # RedisObjectQueue(name="test", redis_url="redis://localhost:6379")
        return "redis://localhost:6379"


# Add items to the queue
queue = MyRedisObjectQueue(name='example_que')
queue.add({'key': 1})
queue.add({'key': 2})
queue.add({'key': 3})
queue.add({'key': 4})
queue.add({'key': 5})

# Can be in separate thread or process
queue = MyRedisObjectQueue(name='example_que')
items = queue.get_items(end=3)
print([item.data for item in items])
# [{'key': 1}, {'key': 2}, {'key': 3}]

print(queue.remove(items))
# 3 - number of items removed

# Can use pop as well
item = queue.pop()
print(item.data)
# {'key': 4}

print(queue.get_total_size())
# 1 - only {'key': 5} is left

# Can prune all the data
queue.prune()
print(queue.get_total_size())
# 0 - nothing left
```

## Authors

This package is developed and maintained by [Thorgate](https://thorgate.eu) as 
part of our effort to change the world with the power of technology. 

See our other projects:
* https://github.com/thorgate
* https://gitlab.com/thorgate-public

## Contributing

To start development, clone the repository and run `make setup`. It expects you to 
have python3.8 and poetry installed.

You will need to set `REDIS_URL` environment variable to run the tests:

```shell
export REDIS_URL=redis://localhost:6379
```

The easiest way to run redis is to run it with Docker:
```shell
docker run --name my-redis-container -p 6379:6379 -d redis
```

Code-formatters are available to make the code more readable and uniform, as well as 
linters to make sure the code is good quality. See Makefile for details. 

The following command will re-format the code
```shell
make black-format-all isort-fix
```

The following command will check the code with linters and tests
```shell
make quality coverage
```

For testing in differnet environments, tox is used. For convenience, tox is ran in
gitlab pipeline.

Please make sure your commit passes all the checks before opening a merge request.

Please consider adding yourself to authors in `pyptoject.toml` if your contribution
is beyond trivial changes.
