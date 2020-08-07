#!/usr/bin/env python

"""Tests for Howdoi."""
import os
import shutil
import unittest
from datetime import datetime
from tempfile import mkdtemp, mkstemp

from cachelib import FileSystemCache, NullCache

from howdoi.stats import (DATE_KEY, DATESTRING_FORMAT, DISCOVERED_LINKS_KEY,
                          HOUR_OF_DAY_KEY, QUERY_KEY, QUERY_WORD_KEY,
                          SEARCH_ENGINE_KEY, Stats)


class StatsTestCase(unittest.TestCase):
    def setUp(self):
        self.cache_dir = mkdtemp(prefix='howdoi_test')
        cache = FileSystemCache(self.cache_dir, default_timeout=0)
        self.stats_obj = Stats(cache)

        self.howdoi_args = [{'query': 'print stack trace python'}, {
            'query': 'check how many cpus on linux'}, {'query': 'battery level on linux ubuntu'}]

        self.result_links = ['https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n', 'https://stackoverflow.com/questions/13427890/how-can-i-find-all-prime-numbers-in-a-given-range',
                             'https://stackoverflow.com/questions/453793/which-is-the-fastest-algorithm-to-find-prime-numbers', 'https://stackoverflow.com/questions/18928095/fastest-way-to-find-all-primes-under-4-billion', ]

    def tearDown(self):
        shutil.rmtree(self.cache_dir)

    def test_days_since_first_install_is_correct(self):
        self.assertEqual(self.stats_obj.get_days_since_first_install(), 0)

    def test_querystring_processing(self):
        for args in self.howdoi_args:
            self.stats_obj.process_query_string(args['query'])

        self.assertIsNotNone(self.stats_obj[QUERY_KEY])
        self.assertIsNotNone(self.stats_obj[QUERY_WORD_KEY])
        for args in self.howdoi_args:
            query = args['query']
            self.assertEquals(self.stats_obj[QUERY_KEY][query], 1)

        self.assertEquals(self.stats_obj[QUERY_WORD_KEY]['linux'], 2)
        self.assertEquals(self.stats_obj[QUERY_WORD_KEY]['python'], 1)
        self.assertEquals(self.stats_obj[QUERY_WORD_KEY]['on'], 0)

    def test_increment_current_date(self):
        self.stats_obj.increment_current_date_count()
        self.stats_obj.increment_current_date_count()
        self.stats_obj.increment_current_date_count()

        curr_date_string = datetime.today().strftime(DATESTRING_FORMAT)

        self.assertIsNotNone(self.stats_obj[DATE_KEY])
        self.assertIs(self.stats_obj[DATE_KEY][curr_date_string], 3)

    def test_increment_current_hour_of_day(self):
        self.stats_obj.increment_current_hour_of_day_count()
        self.stats_obj.increment_current_hour_of_day_count()
        self.stats_obj.increment_current_hour_of_day_count()

        curr_hour_of_day = datetime.now().hour
        self.assertIsNotNone(self.stats_obj[HOUR_OF_DAY_KEY])
        self.assertEquals(self.stats_obj[HOUR_OF_DAY_KEY][curr_hour_of_day], 3)

    def test_process_search_engine(self):
        self.stats_obj.process_search_engine('google')
        self.stats_obj.process_search_engine('google')
        self.stats_obj.process_search_engine('bing')
        self.stats_obj.process_search_engine('bing')

        stored_search_engine_map = self.stats_obj[SEARCH_ENGINE_KEY]

        self.assertEquals(stored_search_engine_map['google'], 2)
        self.assertEquals(stored_search_engine_map['bing'], 2)
        self.assertEquals(stored_search_engine_map['duckduckgo'], 0)

    def test_processes_discovered_links(self):
        self.stats_obj.process_discovered_links(self.result_links)

        stored_links_map = self.stats_obj[DISCOVERED_LINKS_KEY]

        for link in self.result_links:
            self.assertEquals(stored_links_map[link], self.result_links.count(link))


if __name__ == '__main__':
    unittest.main()
