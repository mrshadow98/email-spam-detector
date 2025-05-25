import pickle

from pybloom_live import ScalableBloomFilter


class RedisBloomFilter:
    def __init__(self, redis_client, key='spam_bloom', error_rate=0.001, initial_capacity=10000):
        self.redis = redis_client
        self.key = key
        self._load_or_initialize(error_rate, initial_capacity)

    def _load_or_initialize(self, error_rate, initial_capacity):
        saved_bloom = self.redis.get(self.key)
        if saved_bloom:
            self.bloom = pickle.loads(saved_bloom)
        else:
            self.bloom = ScalableBloomFilter(initial_capacity=initial_capacity, error_rate=error_rate)
            self._persist()

    def _persist(self):
        self.redis.set(self.key, pickle.dumps(self.bloom))

    def add(self, item: str):
        self.bloom.add(item)
        self._persist()

    def __contains__(self, item: str) -> bool:
        return item in self.bloom
