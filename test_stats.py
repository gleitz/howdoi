# testing for stats.py
import unittest
from tempfile import mkdtemp
from cachelib import FileSystemCache
from howdoi.stats import CollectStats


class TestStats(unittest.TestCase):
    def getting_started(self):
        self.cache_dir = mkdtemp(prefix='howdoi_test')
        cache = FileSystemCache(self.cache_dir, default_timeout=0)
        self.stats_obj = CollectStats(cache)
        self.args = [
            {'query': 'print hello in python'},
            {'query': 'create a linked list in python'}
        ]
        # print("tests working yeahhh")


if __name__ == '__main__':
    unittest.main()
