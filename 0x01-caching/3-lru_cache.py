#!/usr/bin/env python3
""" 3-lru_cache.py """
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ a Least Recent Used cache class that imherits from BaseCaching """
    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.lru_order = []

    def put(self, key, item):
        """ Add item to the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if self.lru_order:
                    lru_key = self.lru_order.pop(0)
                    print("DISCARD: {}".format(lru_key))
                    del self.cache_data[lru_key]
            self.cache_data[key] = item
            self.lru_order.append(key)

    def get(self, key):
        """ Get and item by key """
        if key is not None and key in self.cache_data:
            self.lru_order.remove(key)
            self.lru_order.append(key)
            return self.cache_data[key]
        return None
