import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a
    particular function."""
    key_inputs = method.__qualname__ + ":inputs"
    key_outputs = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for decorator."""
        self._redis.rpush(key_inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(key_outputs, str(result))
        return result

    return wrapper


class Cache:
    """Cache class for storing and retrieving data using Redis."""

    def __init__(self):
        """Constructor method for Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method to store data in Redis using a random key and return
        the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
        str, bytes, int, float]:
        """Method to get data from Redis using a key and an optional
        Callable argument named fn."""
        data = self._redis.get(key)
        if data is not None and fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Method to get string data from Redis using a key."""
        data = self.get(key, fn=lambda x: x.decode("utf-8"))
        return data

    def get_int(self, key: str) -> int:
        """Method to get integer data from Redis using a key."""
        data = self.get(key, fn=int)
        return data

    def replay(self, method: Callable):
        """Method to display the history of calls of a particular
        function."""
        inputs = self._redis.lrange(method.__qualname__ + ":inputs", 0, -1)
        outputs = self._redis.lrange(method.__qualname__ + ":outputs", 0,
                                     -1)
        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for inp, out in zip(inputs, outputs):
            print(
                f"{method.__qualname__}{inp.decode('utf-8')} -> {out.decode('utf-8')}")
