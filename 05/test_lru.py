import unittest
from lru import LRUCache


class TestLRU(unittest.TestCase):
    def test_cache(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), None)

    def test_limit(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")

        with self.assertRaises(ValueError):
            cache = LRUCache(0)
            cache.set("k1", "val1")

    def test_double_set(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k1", "val2")
        cache.set("k3", "val3")

        self.assertEqual(cache.get("k1"), "val2")
        self.assertEqual(cache.get("k3"), "val3")
