import requests
import redis
from typing import Callable
from functools import wraps

# Create a Redis client instance
r = redis.Redis()


def count_url_calls(func: Callable) -> Callable:
    """Decorator to count the number of times a URL is accessed."""

    @wraps(func)
    def wrapper(url: str) -> str:
        """Wrapper function for decorator."""
        # Increment the count for the URL
        r.incr(f"count:{url}")
        return func(url)

    return wrapper


@count_url_calls
def get_page(url: str) -> str:
    """Function to get the HTML content of a URL."""
    # Check if the URL is in the cache
    if (cached_page := r.get(url)) is not None:
        return cached_page.decode('utf-8')

    # Get the HTML content of the URL
    page = requests.get(url).text

    # Cache the result with an expiration time of 10 seconds
    r.setex(url, 10, page)

    return page
