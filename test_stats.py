#!/usr/bin/env python

"""Tests for Howdoi."""
import os
import io
import shutil
import unittest
import unittest.mock
from datetime import datetime
from tempfile import mkdtemp, mkstemp

from cachelib import FileSystemCache, NullCache

from howdoi.stats import (DATE_KEY, DATESTRING_FORMAT, DISCOVERED_LINKS_KEY,
                          HOUR_OF_DAY_KEY, QUERY_KEY, QUERY_WORD_KEY,
                          SEARCH_ENGINE_KEY, Stats, Report, StatsReporter, Report, TERMGRAPH_DEFAULT_ARGS, CACHE_HIT_KEY, TOTAL_REQUESTS_KEY, ERROR_RESULT_KEY, SUCCESS_RESULT_KEY)


class StatsTest(unittest.TestCase):
    def setUp(self):
        self.cache_dir = mkdtemp(prefix='howdoi_test')
        cache = FileSystemCache(self.cache_dir, default_timeout=0)
        self.stats_obj = Stats(cache)

        self.howdoi_args = [{'query': 'print stack trace python'}, {
            'query': 'check how many cpus on linux'}, {'query': 'battery level on linux ubuntu'}]

        self.result_links = ['https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n', 'https://stackoverflow.com/questions/13427890/how-can-i-find-all-prime-numbers-in-a-given-range',
                             'https://stackoverflow.com/questions/453793/which-is-the-fastest-algorithm-to-find-prime-numbers', 'https://stackoverflow.com/questions/18928095/fastest-way-to-find-all-primes-under-4-billion', ]

        self.error_howdoi_results = [{"error": "Sorry, couldn\'t find any help with that topic\n"}, {
            "error": "Failed to establish network connection\n"}]
        self.success_howdoi_results = [{'answer': 'https://github.com/<Username>/<Project>.git\n',
                                        'link': 'https://stackoverflow.com/questions/14762034/push-to-github-without-a-password-using-ssh-key', 'position': 1}]

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

    def test_increment_queries_cache_hits(self):
        self.stats_obj.record_cache_hit()
        self.stats_obj.record_cache_hit()
        self.stats_obj.record_cache_hit()

        self.assertEquals(self.stats_obj[CACHE_HIT_KEY], 3)

    def test_total_request_count(self):
        for args in self.howdoi_args:
            self.stats_obj.process_args(args)

        self.assertEquals(self.stats_obj[TOTAL_REQUESTS_KEY], len(self.howdoi_args))

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

    def test_counts_valid_responses(self):
        for response in self.success_howdoi_results:
            self.stats_obj.process_response(response)

        self.assertEquals(self.stats_obj[SUCCESS_RESULT_KEY], len(self.success_howdoi_results))

    def test_counts_error_responses(self):
        for response in self.error_howdoi_results:
            self.stats_obj.process_response(response)

        self.assertEquals(self.stats_obj[ERROR_RESULT_KEY], len(self.error_howdoi_results))


class StatsReporterTest(unittest.TestCase):
    def setUp(self):
        self.sr = StatsReporter(TERMGRAPH_DEFAULT_ARGS)

    def test_add_report(self):
        report_group_name = 'time-stats-group'

        self.sr.add(Report(report_group_name, 'sample stat report'))
        self.assertIn(report_group_name, self.sr._report_group_map)
        self.assertEquals(len(self.sr._report_group_map[report_group_name]), 1)

    def test_add_invalid_report_throws_exception(self):
        with self.assertRaises(AssertionError):
            self.sr.add('sample stat report')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_text_reports_are_rendered_correctly(self, mock_stdout):
        sample_text_report = Report('report-group-1', 'this is a sample stat')
        self.sr.render_report(sample_text_report)
        self.assertEqual(mock_stdout.getvalue(), 'this is a sample stat\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_callable_reports_are_rendered_correctly(self, mock_stdout):
        sample_callable_report = Report('report-group-1', lambda: print('this is a callable stat'))
        self.sr.render_report(sample_callable_report)
        self.assertEqual(mock_stdout.getvalue(), 'this is a callable stat\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_report_separator_render_valid_separator(self, mock_stdout):
        self.sr.render_report_separator(20, '*')
        self.assertEqual(mock_stdout.getvalue(), "*"*20 + "\n")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_overall_report(self, mock_stdout):
        sample_callable_report = Report('report-group-1', lambda: print('this is a callable stat'))
        sample_text_report = Report('report-group-1', 'this is a sample stat')

        self.sr.add(sample_callable_report)
        self.sr.add(sample_text_report)

        self.sr.report()

        self.assertIn("callable", mock_stdout.getvalue())
        self.assertIn("sample", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
