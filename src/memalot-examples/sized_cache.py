"""
Example that creates a cache with a maximum size of 5000 bytes.

Items of size 4096 bytes are stored in the cache. The cache can hold a maximum of one item.
Therefore, the data should be evicted in the next iteration after it is created.

Each iteration lasts 2 seconds, so objects should live for no more than about 4 seconds.
"""

from time import sleep

from cachetools import LRUCache
import numpy as np
from memalot.api import leak_monitor

class DataHolder:
    def __init__(self, data: np.ndarray):
        self._data = data
        self._hash = None  # Cache the hash value

    def __len__(self):
        # Return the actual size in bytes for proper cache sizing
        return self._data.nbytes

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self._data.tobytes())
        return self._hash

# Global cache to avoid passing it as a parameter to the monitored function
cache = LRUCache(maxsize=5000, getsizeof=lambda x: len(x))

@leak_monitor(warmup_calls=2, min_object_age_calls=2)
def create_data(key: int):
    # Create a random numpy array of size 4096 bytes and store it in the cache
    holder = DataHolder(np.random.randint(0, 256, size=(1, 4096), dtype=np.uint8))
    cache[key] = holder

def main():
    for key in range(30):
        create_data(key)
        print(f"Cached data with key {key} and hash {hash(cache[key])}")
        sleep(2.0)

if __name__ == "__main__":
    main()