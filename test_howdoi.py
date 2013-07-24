#!/usr/bin/env python

"""Tests for Howdoi."""

import unittest

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
                        'create tar archive']

    def tearDown(self):
        pass

    def test_get_link_at_pos(self):
        self.assertEqual(howdoi.get_link_at_pos(['/questions/42/'], 1),
                         '/questions/42/')
        self.assertEqual(howdoi.get_link_at_pos(['/questions/42/'], 2),
                         '/questions/42/')
        self.assertEqual(howdoi.get_link_at_pos(['/howdoi', '/questions/42/'], 1),
                         '/questions/42/')
        self.assertEqual(howdoi.get_link_at_pos(['/howdoi', '/questions/42/'], 2),
                         '/questions/42/')
        self.assertEqual(howdoi.get_link_at_pos(['/questions/42/', '/questions/142/'], 1),
                         '/questions/42/')

    def test_answers(self):
        for query in self.queries:
            self.assertTrue(self.call_howdoi(query))

    def test_answers_no_ssl(self):
        for query in self.queries:
            self.assertTrue(self.call_howdoi(query + ' -S'))

    def test_answer_links(self):
        for query in self.queries:
            self.assertTrue('http://' in self.call_howdoi(query + ' -l'))

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
        self.assertTrue("Answer from http://stackoverflow.com" in second_answer)

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

if __name__ == '__main__':
    unittest.main()
