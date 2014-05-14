#!/usr/bin/env python

"""Tests for Howdou."""
import os
import unittest

from howdou import howdou


class HowdouTestCase(unittest.TestCase):

    def call_howdou(self, query):
        parser = howdou.get_parser()
        args = vars(parser.parse_args(query.split(' ')))
        return howdou.howdou(args)

    def setUp(self):
        self.queries = ['format date bash',
                        'print stack trace python',
                        'convert mp4 to animated gif',
                        'create tar archive']
        self.pt_queries = ['abrir arquivo em python',
                           'enviar email em django',
                           'hello world em c']
        self.bad_queries = ['moe',
                            'mel']

    def tearDown(self):
        pass

    def test_get_link_at_pos(self):
        self.assertEqual(howdou.get_link_at_pos(['/questions/42/'], 1),
                         '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/questions/42/'], 2),
                         '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/howdou', '/questions/42/'], 1),
                         '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/howdou', '/questions/42/'], 2),
                         '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/questions/42/', '/questions/142/'], 1),
                         '/questions/42/')

    def test_answers(self):
        for query in self.queries:
            self.assertTrue(self.call_howdou(query))
        for query in self.bad_queries:
            self.assertTrue(self.call_howdou(query))

        os.environ['HOWDOU_LOCALIZATION'] = 'pt-br'
        for query in self.pt_queries:
            self.assertTrue(self.call_howdou(query))

    def test_answer_links(self):
        for query in self.queries:
            self.assertTrue('http://' in self.call_howdou(query + ' -l'))

    def test_position(self):
        query = self.queries[0]
        first_answer = self.call_howdou(query)
        second_answer = self.call_howdou(query + ' -p2')
        self.assertNotEqual(first_answer, second_answer)

    def test_all_text(self):
        query = self.queries[0]
        first_answer = self.call_howdou(query)
        second_answer = self.call_howdou(query + ' -a')
        self.assertNotEqual(first_answer, second_answer)
        self.assertTrue("Answer from http://stackoverflow.com" in second_answer)

    def test_multiple_answers(self):
        query = self.queries[0]
        first_answer = self.call_howdou(query)
        second_answer = self.call_howdou(query + ' -n3')
        self.assertNotEqual(first_answer, second_answer)

    def test_unicode_answer(self):
        assert self.call_howdou('make a log scale d3')
        assert self.call_howdou('python unittest -n3')
        assert self.call_howdou('parse html regex -a')
        assert self.call_howdou('delete remote git branch -a')


class HowdouTestCaseEnvProxies(unittest.TestCase):

    def setUp(self):
        self.temp_get_proxies = howdou.getproxies

    def tearDown(self):
        howdou.getproxies = self.temp_get_proxies

    def test_get_proxies1(self):
        def getproxies1():
            proxies = {'http': 'wwwproxy.company.com',
                       'https': 'wwwproxy.company.com',
                       'ftp': 'ftpproxy.company.com'}
            return proxies

        howdou.getproxies = getproxies1
        filtered_proxies = howdou.get_proxies()
        self.assertTrue('http://' in filtered_proxies['http'])
        self.assertTrue('http://' in filtered_proxies['https'])
        self.assertTrue('ftp' not in filtered_proxies.keys())


if __name__ == '__main__':
    unittest.main()
