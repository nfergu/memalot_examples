from time import sleep

from cachetools import LRUCache
import numpy as np

class DataHolder:
    def __init__(self, data: np.ndarray):
        self._data = data
        # Cache the hash value to avoid recreating bytes objects
        self._hash = hash(data.tobytes())

    def __len__(self):
        # Return the actual size in bytes for proper cache sizing
        return self._data.nbytes

    def __hash__(self):
        return self._hash

def create_data(key: int, cache: LRUCache):
    # Create array with 625 float64 values = 625 * 8 bytes = 5000 bytes
    holder = DataHolder(np.random.rand(1, 625))
    cache[key] = holder

def main():
    # Each DataHolder has a size of 5000. The cache can hold a maximum of 2 items.
    # Therefore, the data should be stored for a maximum of 2 iterations.
    cache = LRUCache(maxsize=10000, getsizeof=lambda x: len(x))
    for key in range(50):
        create_data(key, cache)
        print(f"Cached data with key {key} and hash {hash(cache[key])}")
        sleep(2.0)

if __name__ == "__main__":
    main()