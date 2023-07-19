import requests
import time

# Dictionary to store cached results and access counts
cache = {}


def cache_result(expiration_time):
    def decorator(func):
        def wrapper(url):
            # Check if the URL is already in the cache and not expired
            if url in cache and time.time() - cache[url]["timestamp"] < expiration_time:
                print("Using cached result for:", url)
                cache[url]["count"] += 1
                return cache[url]["content"]
            else:
                print("Fetching from the web for:", url)
                content = func(url)
                # Update the cache
                cache[url] = {
                    "content": content,
                    "timestamp": time.time(),
                    "count": 1,
                }
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
