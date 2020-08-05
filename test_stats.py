#!/usr/bin/env python

"""Tests for Howdoi."""
import os
import shutil
import unittest
from datetime import datetime
from tempfile import mkdtemp, mkstemp

from cachelib import FileSystemCache, NullCache

from howdoi.stats import Keys, Stats

# class StoreTestCase(unittest.TestCase):
#     def setUp(self):
#         self.store_dir = mkdtemp(prefix='howdoi_test')
#         self.store = Store(self.store_dir)

#     def tearDown(self):
#         shutil.rmtree(self.store_dir)

#     def test_store_start_date_is_set(self):
#         store_start_date = self.store[Keys.FIRST_INSTALL_DATE]
#         self.assertIsNotNone(store_start_date)
#         self.assertEquals(store_start_date, datetime.today().strftime("%Y-%m-%d"))


class StatsTestCase(unittest.TestCase):
    def setUp(self):
        self.cache_dir = mkdtemp(prefix='howdoi_test')
        cache = FileSystemCache(self.cache_dir, default_timeout=0)
        self.stats_obj = Stats(cache)

        self.args = [
            {'query': 'print stack trace python'},
            {'query': 'check how many cpus on linux'},
            {'query': 'battery level on linux ubuntu'}

        ]

    def tearDown(self):
        shutil.rmtree(self.cache_dir)

    def test_days_since_first_install_is_correct(self):
        self.assertEqual(self.stats_obj.get_days_since_first_install(), 0)

    def test_querystring_processing(self):
        for args in self.args:
            self.stats_obj.process_query_string(args['query'])

        self.assertEqual(self.stats_obj[Keys.QUERY_COUNT_PREFIX+'linux'], 2)
        self.assertEqual(self.stats_obj[Keys.QUERY_COUNT_PREFIX+'python'], 1)
        self.assertEqual(self.stats_obj[Keys.QUERY_COUNT_PREFIX+'on'], None)

    def test_store_current_hour_of_day(self):
        self.stats_obj.store_current_hour_of_day()
        self.stats_obj.store_current_hour_of_day()
        self.stats_obj.store_current_hour_of_day()

        curr_hour_of_day = str(datetime.now().hour)
        self.assertEqual(self.stats_obj[Keys.HOUR_OF_DAY_PREFIX+curr_hour_of_day], 3)


if __name__ == '__main__':
    unittest.main()
