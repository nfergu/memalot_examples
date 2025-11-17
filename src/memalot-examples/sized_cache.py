from time import sleep

from cachetools import LRUCache
import numpy as np
from memalot import api

class DataHolder:
    def __init__(self, data: np.ndarray):
        self._data = data

    def __len__(self):
        # Return the actual size in bytes for proper cache sizing
        return self._data.nbytes

    def __hash__(self):
        return hash(self._data.tobytes())

def create_data(key: int, cache: LRUCache):
    # Create array with 625 float64 values = 625 * 8 bytes = 5000 bytes
    holder = DataHolder(np.random.rand(1, 625))
    cache[key] = holder

def main():
    # Start time-based leak monitoring focusing on bytes objects
    # Objects that survive for more than 2 seconds are considered leaks
    # Warmup time is 0.5 seconds
    monitor = api.start_leak_monitoring(
        max_object_lifetime=2.0,
        warmup_time=0.5,
        save_reports=True,
        check_referrers=True,
        included_type_names={"bytes", "ndarray", "DataHolder"}
    )
    
    # Each DataHolder has a size of 5000. The cache can hold a maximum of 2 items.
    # Therefore, the data should be stored for a maximum of 2 iterations.
    cache = LRUCache(maxsize=10000, getsizeof=lambda x: len(x))
    for key in range(30):  # Reduced from 50 to 30 for faster testing
        create_data(key, cache)
        print(f"Cached data with key {key} and hash {hash(cache[key])}")
        sleep(0.5)
    
    monitor.stop()

if __name__ == "__main__":
    main()