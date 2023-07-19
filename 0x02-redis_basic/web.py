#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
import time
import redis

# Create a Redis instance
redis_store = redis.Redis()


def cache_result(expiration_time):
    def decorator(func):
        def wrapper(url):
            # Check if the URL is already in the Redis cache and not expired
            cached_content = redis_store.get(f'content:{url}')
            if cached_content:
                print("Using cached result for:", url)
                # Update the access count in Redis
                redis_store.incr(f'count:{url}')
                return cached_content.decode("utf-8")
            else:
                print("Fetching from the web for:", url)
                content = func(url)
                # Store the result in Redis with an expiration time
                redis_store.setex(f'content:{url}', expiration_time, content)
                # Initialize the access count in Redis to 1
                redis_store.set(f'count:{url}', 1)
                return content

        return wrapper

    return decorator


@cache_result(expiration_time=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Test the get_page function with a slow URL
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    print(get_page(url))
    print(get_page(url))  # Should use the cached result and not fetch again for the same URL
    time.sleep(11)  # Wait for cache to expire
    print(get_page(url))  # Should fetch again as cache has expired
