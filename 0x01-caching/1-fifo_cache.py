#!/usr/bin/env python3
""" 1-fifo_cache.py """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ a FIFO cache class that inherits from BaseCaching """
    def __init__(self):
        """ Initialize the FIFO Cache """
        super().__init__()

    def put(self, key, item):
        """ Add items in the cahce """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                first_key = next(iter(self.cache_data))
                print("DISCARD: {}".format(first_key))
                del self.cache_data[first_key]
            self.cache_data[key] = item

    def get(self, key):
        """ get an item by key """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
