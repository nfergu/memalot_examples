"""
Example that creates a cache with a maximum size of 5000 bytes.

Items of size 4096 bytes are stored in the cache. The cache can hold a maximum of one item.
Therefore, the data should be evicted in the next iteration after it is created.

Each iteration lasts 2 seconds, so objects should live for no more than about 4 seconds.
"""

from time import sleep

from cachetools import LRUCache
import numpy as np
from memalot.api import start_leak_monitoring

class DataHolder:
    def __init__(self, data: np.ndarray):
        self._data = data

    def __len__(self):
        # Return the actual size in bytes for proper cache sizing
        return len(self._data)

    def __hash__(self):
        return hash(self._data.tobytes())

def create_data(key: int, cache: LRUCache):
    # Create a random numpy array of size 4906 bytes and store it in the cache
    holder = DataHolder(np.random.randint(0, 256, size=(1, 4096), dtype=np.uint8))
    cache[key] = holder

def main():
    # Start Memalot time-based monitoring
    # Objects should live for no more than 4 seconds (2 iterations)
    # Set max_object_lifetime to 4 seconds and warmup to 4 seconds
    start_leak_monitoring(max_object_lifetime=4.0, warmup_time=4.0)
    
    cache = LRUCache(maxsize=5000, getsizeof=lambda x: len(x))
    for key in range(30):
        create_data(key, cache)
        print(f"Cached data with key {key} and hash {hash(cache[key])}")
        sleep(2.0)

if __name__ == "__main__":
    main()