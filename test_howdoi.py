#!/usr/bin/env python

"""Tests for Howdoi."""
import gzip
import json
import os
import re
import unittest
from pathlib import Path
from cachelib import NullCache
from pyquery import PyQuery as pq

# pylint: disable=no-name-in-module
from howdoi import howdoi


# pylint: disable=protected-access
class HowdoiTestCase(unittest.TestCase):  # pylint: disable=too-many-public-methods
    def _get_result_mock(self, url):
        file_name = howdoi._format_url_to_filename(url, 'html.gz')
        # pylint: disable=no-member
        file_path = Path.joinpath(Path(howdoi.HTML_CACHE_PATH), Path(file_name)).resolve()
        try:
            with gzip.open(file_path, 'rb') as f:
                cached_page_content = str(f.read(), encoding='utf-8')
                return cached_page_content

        except FileNotFoundError:
            page_content = self.original_get_result(url)
            with gzip.open(file_path, 'wb') as f:
                f.write(bytes(page_content, encoding='utf-8'))
                return page_content

    def _negative_number_query(self):
        query = self.queries[0]
        howdoi.howdoi(query + ' -n -1')

    def _high_positive_number_query(self):
        query = self.queries[0]
        howdoi.howdoi(query + ' -n 21')

    def _negative_position_query(self):
        query = self.queries[0]
        howdoi.howdoi(query + ' -p -2')

    def _high_positive_position_query(self):
        query = self.queries[0]
        howdoi.howdoi(query + ' -p 40')

    def setUp(self):
        self.original_get_result = howdoi._get_result
        howdoi._get_result = self._get_result_mock

        # ensure no cache is used during testing.
        howdoi.cache = NullCache()

        self.queries = ['format date bash',
                        'print stack trace python',
                        'convert mp4 to animated gif',
                        'create tar archive',
                        'cat']
        self.help_queries = howdoi.SUPPORTED_HELP_QUERIES
        self.pt_queries = ['abrir arquivo em python',
                           'enviar email em django',
                           'hello world em c']
        self.bad_queries = ['moe',
                            'mel']
        self.query_without_code_or_pre_block = 'Difference between element node and Text Node'

    def assertValidResponse(self, res):  # pylint: disable=invalid-name
        self.assertTrue(len(res) > 0)

    def tearDown(self):
        keys_to_remove = ['HOWDOI_URL', 'HOWDO_SEARCH_ENGINE']
        for key in keys_to_remove:
            if key in os.environ:
                del os.environ[key]

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
            self.assertValidResponse(howdoi.howdoi(query))
        for query in self.bad_queries:
            self.assertValidResponse(howdoi.howdoi(query))

        os.environ['HOWDOI_URL'] = 'pt.stackoverflow.com'
        for query in self.pt_queries:
            self.assertValidResponse(howdoi.howdoi(query))

    def test_answers_bing(self):
        os.environ['HOWDOI_SEARCH_ENGINE'] = 'bing'
        for query in self.queries:
            self.assertValidResponse(howdoi.howdoi(query))
        for query in self.bad_queries:
            self.assertValidResponse(howdoi.howdoi(query))

        os.environ['HOWDOI_URL'] = 'pt.stackoverflow.com'
        for query in self.pt_queries:
            self.assertValidResponse(howdoi.howdoi(query))

        os.environ['HOWDOI_SEARCH_ENGINE'] = ''

    def test_answers_duckduckgo(self):
        os.environ['HOWDOI_SEARCH_ENGINE'] = 'duckduckgo'
        for query in self.queries:
            self.assertValidResponse(howdoi.howdoi(query))
        for query in self.bad_queries:
            self.assertValidResponse(howdoi.howdoi(query))

        os.environ['HOWDOI_URL'] = 'pt.stackoverflow.com'
        for query in self.pt_queries:
            self.assertValidResponse(howdoi.howdoi(query))

        os.environ['HOWDOI_SEARCH_ENGINE'] = ''

    def test_answer_links_using_l_option(self):
        for query in self.queries:
            response = howdoi.howdoi(query + ' -l')
            self.assertNotEqual(re.match(r'http.?://.*questions/\d.*', response, re.DOTALL), None)

    def test_answer_links_using_all_option(self):
        for query in self.queries:
            response = howdoi.howdoi(query + ' -a')
            self.assertNotEqual(re.match(r'.*http.?://.*questions/\d.*', response, re.DOTALL), None)

    def test_position(self):
        query = self.queries[0]
        first_answer = howdoi.howdoi(query)
        not_first_answer = howdoi.howdoi(query + ' -p5')
        self.assertNotEqual(first_answer, not_first_answer)

    def test_all_text(self):
        query = self.queries[0]
        first_answer = howdoi.howdoi(query)
        second_answer = howdoi.howdoi(query + ' -a')
        self.assertNotEqual(first_answer, second_answer)
        self.assertNotEqual(re.match('.*Answer from http.?://.*', second_answer, re.DOTALL), None)

    def test_json_output(self):
        query = self.queries[0]
        txt_answer = howdoi.howdoi(query)
        json_answer = howdoi.howdoi(query + ' -j')
        link_answer = howdoi.howdoi(query + ' -l')
        json_answer = json.loads(json_answer)[0]
        self.assertEqual(json_answer["answer"], txt_answer)
        self.assertEqual(json_answer["link"], link_answer)
        self.assertEqual(json_answer["position"], 1)

    def test_multiple_answers(self):
        query = self.queries[0]
        first_answer = howdoi.howdoi(query)
        second_answer = howdoi.howdoi(query + ' -n3')
        self.assertNotEqual(first_answer, second_answer)

    def test_unicode_answer(self):  # pylint: disable=no-self-use
        assert howdoi.howdoi('make a log scale d3')
        assert howdoi.howdoi('python unittest -n3')
        assert howdoi.howdoi('parse html regex -a')
        assert howdoi.howdoi('delete remote git branch -a')

    def test_colorize(self):
        query = self.queries[0]
        normal = howdoi.howdoi(query)
        colorized = howdoi.howdoi('-c ' + query)
        self.assertTrue(normal.find('[39;') == -1)
        self.assertTrue(colorized.find('[39;') != -1)

    # pylint: disable=line-too-long
    def test_get_text_without_links(self):
        html = '''\n  <p>The halting problem is basically a\n  formal way of asking if you can tell\n  whether or not an arbitrary program\n  will eventually halt.</p>\n  \n  <p>In other words, can you write a\n  program called a halting oracle,\n  HaltingOracle(program, input), which\n  returns true if program(input) would\n  eventually halt, and which returns\n  false if it wouldn't?</p>\n  \n  <p>The answer is: no, you can't.</p>\n'''  # noqa: E501
        paragraph = pq(html)
        expected_output = '''The halting problem is basically a\n  formal way of asking if you can tell\n  whether or not an arbitrary program\n  will eventually halt.\n\n  \n  \nIn other words, can you write a\n  program called a halting oracle,\n  HaltingOracle(program, input), which\n  returns true if program(input) would\n  eventually halt, and which returns\n  false if it wouldn't?\n\n  \n  \nThe answer is: no, you can't.\n\n'''  # noqa: E501
        actual_output = howdoi.get_text(paragraph)
        self.assertEqual(actual_output, expected_output)

    def test_get_text_with_one_link(self):
        html = '<p>It\'s a <a href="http://paulirish.com/2010/the-protocol-relative-url/">protocol-relative URL</a> (typically HTTP or HTTPS). So if I\'m on <code>http://example.org</code> and I link (or include an image, script, etc.) to <code>//example.com/1.png</code>, it goes to <code>http://example.com/1.png</code>. If I\'m on <code>https://example.org</code>, it goes to <code>https://example.com/1.png</code>.</p>'  # noqa: E501
        paragraph = pq(html)
        expected_output = "It's a [protocol-relative URL](http://paulirish.com/2010/the-protocol-relative-url/) (typically HTTP or HTTPS). So if I'm on http://example.org and I link (or include an image, script, etc.) to //example.com/1.png, it goes to http://example.com/1.png. If I'm on https://example.org, it goes to https://example.com/1.png."  # noqa: E501
        actual_output = howdoi.get_text(paragraph)
        self.assertEqual(actual_output, expected_output)

    def test_get_text_with_multiple_links_test_one(self):
        html = 'Here\'s a quote from <a href="http://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style#Links" rel="nofollow noreferrer">wikipedia\'s manual of style</a> section on links (but see also <a href="http://en.wikipedia.org/wiki/Wikipedia:External_links" rel="nofollow noreferrer">their comprehensive page on External Links</a>)'  # noqa: E501
        paragraph = pq(html)
        expected_output = "Here's a quote from [wikipedia's manual of style](http://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style#Links) section on links (but see also [their comprehensive page on External Links](http://en.wikipedia.org/wiki/Wikipedia:External_links))"  # noqa: E501
        actual_output = howdoi.get_text(paragraph)
        self.assertEqual(actual_output, expected_output)

    def test_get_text_with_multiple_links_test_two(self):
        html = 'For example, if I were to reference <a href="http://www.apple.com/" rel="nofollow noreferrer">apple.com</a> as the subject of a sentence - or to talk about <a href="http://www.apple.com/" rel="nofollow noreferrer">Apple\'s website</a> as the topic of conversation. This being different to perhaps recommendations for reading <a href="https://ux.stackexchange.com/q/14872/6046">our article about Apple\'s website</a>.'  # noqa: E501
        paragraph = pq(html)
        expected_output = "For example, if I were to reference [apple.com](http://www.apple.com/) as the subject of a sentence - or to talk about [Apple's website](http://www.apple.com/) as the topic of conversation. This being different to perhaps recommendations for reading [our article about Apple's website](https://ux.stackexchange.com/q/14872/6046)."  # noqa: E501
        actual_output = howdoi.get_text(paragraph)
        self.assertEqual(actual_output, expected_output)

    def test_get_text_with_link_but_with_copy_duplicating_the_href(self):
        html = '<a href="https://github.com/jquery/jquery/blob/56136897f241db22560b58c3518578ca1453d5c7/src/manipulation.js#L451" rel="nofollow noreferrer">https://github.com/jquery/jquery/blob/56136897f241db22560b58c3518578ca1453d5c7/src/manipulation.js#L451</a>'  # noqa: E501
        paragraph = pq(html)
        expected_output = 'https://github.com/jquery/jquery/blob/56136897f241db22560b58c3518578ca1453d5c7/src/manipulation.js#L451'  # noqa: E501
        actual_output = howdoi.get_text(paragraph)
        self.assertEqual(actual_output, expected_output)

    def test_get_text_with_a_link_but_copy_is_within_nested_div(self):
        html = 'If the function is from a source file available on the filesystem, then <a href="https://docs.python.org/3/library/inspect.html#inspect.getsource" rel="noreferrer"><code>inspect.getsource(foo)</code></a> might be of help:'  # noqa: E501
        paragraph = pq(html)
        expected_output = 'If the function is from a source file available on the filesystem, then [inspect.getsource(foo)](https://docs.python.org/3/library/inspect.html#inspect.getsource) might be of help:'  # noqa: E501
        actual_output = howdoi.get_text(paragraph)
        self.assertEqual(actual_output, expected_output)
    # pylint: enable=line-too-long

    def test_get_questions(self):
        links = ['https://stackoverflow.com/questions/tagged/cat',
                 'http://rads.stackoverflow.com/amzn/click/B007KAZ166',
                 'https://stackoverflow.com/questions/40108569/how-to-get-the-last-line-of-a-file-using-cat-command']
        expected_output = [
            'https://stackoverflow.com/questions/40108569/how-to-get-the-last-line-of-a-file-using-cat-command']
        actual_output = howdoi._get_questions(links)
        self.assertSequenceEqual(actual_output, expected_output)

    def test_help_queries(self):
        help_queries = self.help_queries

        for query in help_queries:
            output = howdoi.howdoi(query)
            self.assertTrue(output)
            self.assertIn('few popular howdoi commands', output)
            self.assertIn('retrieve n number of answers', output)
            self.assertIn(
                'Specify the search engine you want to use e.g google,bing',
                output
            )

    def test_missing_pre_or_code_query(self):
        output = howdoi.howdoi(self.query_without_code_or_pre_block)
        self.assertTrue(output)
        self.assertIn('XML elements present in a XML', output)

    def test_format_url_to_filename(self):
        url = 'https://stackoverflow.com/questions/tagged/cat'
        invalid_filename_characters = ['/', '\\', '%']
        filename = howdoi._format_url_to_filename(url, 'html')
        self.assertTrue(filename)
        self.assertTrue(filename.endswith('html'))
        for invalid_character in invalid_filename_characters:
            self.assertNotIn(invalid_character, filename)

    def test_help_queries_are_properly_validated(self):
        help_queries = self.help_queries
        for query in help_queries:
            is_valid_help_query = howdoi._is_help_query(query)
            self.assertTrue(is_valid_help_query)
        bad_help_queries = [self.queries[0],
                            self.bad_queries[0], 'use how do i']

        for query in bad_help_queries:
            self.assertFalse(howdoi._is_help_query(query))

    def test_negative_and_high_positive_int_values_rejected(self):
        with self.assertRaises(SystemExit):
            self._negative_number_query()
        with self.assertRaises(SystemExit):
            self._negative_position_query()
        with self.assertRaises(SystemExit):
            self._high_positive_position_query()
        with self.assertRaises(SystemExit):
            self._high_positive_number_query()


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
