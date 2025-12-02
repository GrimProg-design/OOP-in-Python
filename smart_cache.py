import time

class CacheItem:
    def __init__(self, key, value, ttl=None, priority=1):
        self.key = key
        self.value = value
        self.creation_time = time.time()
        self.last_access_time = self.creation_time
        self.access_count = 0
        self.priority = priority
        self.ttl = ttl

    def access(self):
        self.last_access_time = time.time()
        self.access_count += 1

    def is_expired(self):
        if self.ttl is None:
            return False
        return (time.time() - self.creation_time) > self.ttl
    
class EvictionPolicy:
    def select_victim(self, cache_items):
        raise NotImplementedError("Метод select_victim() должен быть реализован")
    
class LRUPolicy(EvictionPolicy):
    def select_victim(self, cache_items):
        return min(cache_items, key=lambda item: item.last_access_time)
    
class LFUPolicy(EvictionPolicy):
    def select_victim(self, cache_items):
        return min(cache_items, key=lambda item: item.access_count)
    

class FIFOPolicy(EvictionPolicy):
    def select_victim(self, cache_items):
        return min(cache_items, key=lambda item: item.creation_time)

class PriorityPolicy(EvictionPolicy):
    def select_victim(self, cache_items):
        low = [i for i in cache_items if i.priority <= 1]
        if low:
            return min(low, key=lambda i: i.priority)
        return min(cache_items, key=lambda i: i.priority)
    
class AdaptivePolicy(EvictionPolicy):
    def __init__(self, cache):
        self.cache = cache

    def select_victim(self, cache_items):
        rate = self.cache.statistics["hit_rate"]

        if rate < 0.3:
            policy = LRUPolicy()
        elif rate < 0.6:
            policy = LFUPolicy()
        else:
            policy = PriorityPolicy()

        return policy.select_victim(cache_items)
    
class SmartCache:
    def __init__(self, max_size=5, max_memory=9999, eviction_policy=None):
        self.max_size = max_size
        self.max_memory = max_memory
        self.items = {}
        self.eviction_policy = eviction_policy or LRUPolicy()

        self.statistics = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "hit_rate": 0
        }

    def __getitem__(self, key):
        if key not in self.items:
            self.statistics["misses"] += 1
            self._update_hit_rate()
            return None

        item = self.items[key]

        if item.is_expired():
            del self.items[key]
            self.statistics["misses"] += 1
            self._update_hit_rate()
            return None

        item.access()
        self.statistics["hits"] += 1
        self._update_hit_rate()
        return item.value


    def __setitem__(self, key, value):
        self.set(key, value)


    def __delitem__(self, key):
        if key in self.items:
            del self.items[key]


    def __contains__(self, key):
        return key in self.items


    def __len__(self):
        return len(self.items)


    def __iter__(self):
        return iter(self.items.keys())
    
    def set(self, key, value, ttl=None, priority=1):
        if len(self.items) >= self.max_size:
            self._evict()

        item = CacheItem(key, value, ttl, priority)
        self.items[key] = item


    def get(self, key, default=None):
        res = self.__getitem__(key)
        return res if res is not None else default


    def _update_hit_rate(self):
        total = self.statistics["hits"] + self.statistics["misses"]
        self.statistics["hit_rate"] = self.statistics["hits"] / total if total else 0


    def _evict(self):
        cache_items = list(self.items.values())
        victim = self.eviction_policy.select_victim(cache_items)

        if victim.priority >= 10:
            low = [i for i in cache_items if i.priority < 10]
            if not low: return
            victim = self.eviction_policy.select_victim(low)

        del self.items[victim.key]
        self.statistics["evictions"] += 1


    def clear(self):
        self.items = {}
        self.statistics = {"hits": 0, "misses": 0, "evictions": 0, "hit_rate": 0}


    def get_statistics(self):
        return self.statistics


    def set_policy(self, policy):
        self.eviction_policy = policy


    def get_memory_usage(self):
        return len(self.items) * 64
    
cache = SmartCache(max_size=3, eviction_policy=LRUPolicy())

cache.set("A", 1)
cache.set("B", 2)
cache.set("C", 3)

print(cache["A"])
cache.set("D", 4)

print("\nСодержимое:", list(cache))
print("Статистика:", cache.get_statistics())

cache.set_policy(AdaptivePolicy(cache))
cache.set("X", 10)
cache.set("Y", 11)
cache.set("Z", 12)

print("\nПосле AdaptivePolicy:", list(cache))
print("Статистика:", cache.get_statistics())