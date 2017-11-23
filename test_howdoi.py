#!/usr/bin/env python

"""Tests for Howdoi."""
import os
import unittest
import re
import sys

from howdoi import howdoi


class HowdoiTestCase(unittest.TestCase):

    def call_howdoi(self, query):
        parser = howdoi.get_parser()
        args = vars(parser.parse_args(query.split(' ')))
        return howdoi.howdoi(args)

    def setUp(self):
        self.queries = ['format date bash',
                        'print stack trace python',
                        'convert mp4 to animated gif',
                        'create tar archive',
                        'cat']
        self.pt_queries = ['abrir arquivo em python',
                           'enviar email em django',
                           'hello world em c']
        self.bad_queries = ['moe',
                            'mel']

    def tearDown(self):
        pass

    def test_get_link_at_pos(self):
        self.assertEqual(howdoi.get_link_at_pos(['/questions/42/'], 1),
                         '/questions/42/')
        self.assertEqual(howdoi.get_link_at_pos(['/questions/42/'], 2),
                         '/questions/42/')
        self.assertEqual(howdoi.get_link_at_pos(['/howdoi', '/questions/42/'], 1),
                         '/howdoi')
        self.assertEqual(howdoi.get_link_at_pos(['/howdoi', '/questions/42/'], 2),
                         '/questions/42/')
        self.assertEqual(howdoi.get_link_at_pos(['/questions/42/', '/questions/142/'], 1),
                         '/questions/42/')

    def test_answers(self):
        for query in self.queries:
            self.assertTrue(self.call_howdoi(query))
        for query in self.bad_queries:
            self.assertTrue(self.call_howdoi(query))

        os.environ['HOWDOI_URL'] = 'pt.stackoverflow.com'
        for query in self.pt_queries:
            self.assertTrue(self.call_howdoi(query))

    def test_answer_links_using_l_option(self):
        for query in self.queries:
            response = self.call_howdoi(query + ' -l')
            self.assertNotEqual(re.match('http.?://.*questions/\d.*', response, re.DOTALL), None)

    def test_answer_links_using_all_option(self):
        for query in self.queries:
            response = self.call_howdoi(query + ' -a')
            self.assertNotEqual(re.match('.*http.?://.*questions/\d.*', response, re.DOTALL), None)

    def test_position(self):
        query = self.queries[0]
        first_answer = self.call_howdoi(query)
        second_answer = self.call_howdoi(query + ' -p2')
        self.assertNotEqual(first_answer, second_answer)

    def test_all_text(self):
        query = self.queries[0]
        first_answer = self.call_howdoi(query)
        second_answer = self.call_howdoi(query + ' -a')
        self.assertNotEqual(first_answer, second_answer)
        self.assertNotEqual(re.match('.*Answer from http.?://.*', second_answer, re.DOTALL), None)

    def test_multiple_answers(self):
        query = self.queries[0]
        first_answer = self.call_howdoi(query)
        second_answer = self.call_howdoi(query + ' -n3')
        self.assertNotEqual(first_answer, second_answer)

    def test_unicode_answer(self):
        assert self.call_howdoi('make a log scale d3')
        assert self.call_howdoi('python unittest -n3')
        assert self.call_howdoi('parse html regex -a')
        assert self.call_howdoi('delete remote git branch -a')

    def test_colorize(self):
        query = self.queries[0]
        normal = self.call_howdoi(query)
        colorized = self.call_howdoi('-c ' + query)
        self.assertTrue(normal.find('[39;') is -1)
        self.assertTrue(colorized.find('[39;') is not -1)

    def test_get_questions(self):
        links = ['https://stackoverflow.com/questions/tagged/cat', 'http://rads.stackoverflow.com/amzn/click/B007KAZ166', 'https://stackoverflow.com/questions/40108569/how-to-get-the-last-line-of-a-file-using-cat-command']
        expected_output = ['https://stackoverflow.com/questions/40108569/how-to-get-the-last-line-of-a-file-using-cat-command']
        actual_output = howdoi._get_questions(links)
        if sys.version < '2.7':
            self.assertEqual(len(actual_output), len(expected_output))
            self.assertEqual(sorted(actual_output), sorted(expected_output))
        else:
            self.assertSequenceEqual(actual_output, expected_output)


class HowdoiTestCaseEnvProxies(unittest.TestCase):

    def setUp(self):
        self.temp_get_proxies = howdoi.getproxies

    def tearDown(self):
        howdoi.getproxies = self.temp_get_proxies

    def test_get_proxies1(self):
        def getproxies1():
            proxies = {'http': 'wwwproxy.company.com',
                       'https': 'wwwproxy.company.com',
                       'ftp': 'ftpproxy.company.com'}
            return proxies

        howdoi.getproxies = getproxies1
        filtered_proxies = howdoi.get_proxies()
        self.assertTrue('http://' in filtered_proxies['http'])
        self.assertTrue('http://' in filtered_proxies['https'])
        self.assertTrue('ftp' not in filtered_proxies.keys())


if __name__ == '__main__':
    unittest.main()
