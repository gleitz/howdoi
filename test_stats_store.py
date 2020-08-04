#!/usr/bin/env python

"""Tests for Howdoi."""
import unittest
import shutil
import os
from howdoi.stats import Store, Keys, Stats
from datetime import datetime
from tempfile import mkstemp, mkdtemp


class StoreTestCase(unittest.TestCase):
    def setUp(self):
        self.store_dir = mkdtemp(prefix='howdoi_test')
        self.store = Store(self.store_dir)

    def tearDown(self):
        shutil.rmtree(self.store_dir)

    def test_store_start_date_is_set(self):
        store_start_date = self.store[Keys.FIRST_INSTALL_DATE]
        self.assertIsNotNone(store_start_date)
        self.assertEquals(store_start_date, datetime.today().strftime("%Y-%m-%d"))


class StatsTestCase(unittest.TestCase):
    def setUp(self):
        self.store_dir = mkdtemp(prefix='howdoi_test')
        self.stats_obj = Stats(Store(self.store_dir))

    def tearDown(self):
        shutil.rmtree(self.store_dir)

    def test_days_since_first_install_is_correct(self):
        self.assertEqual(self.stats_obj.get_days_since_first_install(), 0)


if __name__ == '__main__':
    unittest.main()
