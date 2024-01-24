#!/usr/bin/env python3
"""
Redis tutorial
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def parse_line(line: str, total_size: int, status_codes: dict) -> tuple:
    """
    this method Parses log line and update total_size and status_codes.
    """
    try:
        parts = line.split()
        size = int(parts[-1])
        code = int(parts[-2])
        total_size += size

        if code in status_codes:
            status_codes[code] += 1
        return total_size, status_codes
    except (ValueError, IndexError):
        return total_size, status_codes


class Cache:
    """
    Class cache for data storing
    """

    def __init__(self) -> None:
        """
        method, store an instance of the Redis client as a private
        variable named _redis (using redis.Redis()) and flush the
        instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key, stores the input data in Redis using the key
        and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        this method that take a key string argument and an optional
        Callable
        argument named fn"""
        result = self._redis.get(key)
        if result and fn:
            return fn(result)
        return result

    def get_str(self, key: str) -> str:
        """
        Retrieves data from Redis as a string.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieves data from Redis as an integer.
        """
        return self.get(key, fn=int)

    def increment(self, key: str) -> int:
        """
        Increments the value stored at the specified key in Redis.
        """
        return self._redis.incr(key)

    def call_history(method: Callable) -> Callable:
        """
        this Decorator to store the history of inputs and outputs for a
        function.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            """
            This Wrapper function to store input and output history
            and call the original method.
            """
            input_key = "{}:inputs".format(method.__qualname__)
            output_key = "{}:outputs".format(method.__qualname__)

            self._redis.rpush(input_key, str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(result))

            return result

        return wrapper

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        this method generates a random key, stores the input data in
        Redis using the key
        and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(self, method: Callable) -> None:
        """
        this function displays the history of calls of a particular
        function.
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)

        print(
            "{} was called {} times:".format(
                method.__qualname__, len(inputs)))

        for inp, out in zip(inputs, outputs):
            print("{} -> {}".format(inp, out))
