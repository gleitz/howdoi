#!/usr/bin/env python

"""Tests for Howdoi."""
import os
import shutil
import unittest
from datetime import datetime
from tempfile import mkdtemp, mkstemp

from cachelib import FileSystemCache, NullCache

from howdoi.stats import Stats, QUERY_COUNT_PREFIX, DATE_KEY_PREFIX, DATESTRING_FORMAT, HOUR_OF_DAY_KEY_PREFIX, SEARCH_ENGINE_KEY


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

        self.assertEqual(self.stats_obj[QUERY_COUNT_PREFIX+'linux'], 2)
        self.assertEqual(self.stats_obj[QUERY_COUNT_PREFIX+'python'], 1)
        self.assertEqual(self.stats_obj[QUERY_COUNT_PREFIX+'on'], None)

    def test_increment_current_date(self):
        self.stats_obj.increment_current_date_count()
        self.stats_obj.increment_current_date_count()
        self.stats_obj.increment_current_date_count()

        curr_date_string = datetime.today().strftime(DATESTRING_FORMAT)

        self.assertIsNotNone(self.stats_obj[DATE_KEY_PREFIX+curr_date_string])
        self.assertIs(self.stats_obj[DATE_KEY_PREFIX+curr_date_string], 3)

    def test_increment_current_hour_of_day(self):
        self.stats_obj.increment_current_hour_of_day_count()
        self.stats_obj.increment_current_hour_of_day_count()
        self.stats_obj.increment_current_hour_of_day_count()

        curr_hour_of_day = datetime.now().hour
        key = HOUR_OF_DAY_KEY_PREFIX + str(curr_hour_of_day)
        self.assertEquals(self.stats_obj[key], 3)

    def test_process_search_engine(self):
        self.stats_obj.process_search_engine('google')
        self.stats_obj.process_search_engine('google')
        self.stats_obj.process_search_engine('bing')
        self.stats_obj.process_search_engine('bing')

        stored_search_engine_map = self.stats_obj[SEARCH_ENGINE_KEY]

        self.assertEquals(stored_search_engine_map['google'], 2)
        self.assertEquals(stored_search_engine_map['bing'], 2)
        self.assertEquals(stored_search_engine_map['duckduckgo'], 0)


if __name__ == '__main__':
    unittest.main()
