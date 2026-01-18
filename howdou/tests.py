#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import unittest
from unittest import TestCase as _TestCase
from pprint import pprint
import traceback
import tempfile
import shutil

import yaml

from . import howdou
from .howdou import (
    HowDoU,
    get_parser,
    _sanitize_index_name,
    _build_fts_query,
    _rank_to_score,
    _compute_file_hash,
    _build_entry_id,
)


def _getattribute(cls, self, attrname):

    # Wrap test methods so we can capture their exceptions.
    # The default unittest framework doesn't make this easy.

    def test_wrap(func):
        def _wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print('!'*80, file=sys.stderr)
                print('An exception was encountered in test method %s.' \
                    % self._testMethodName, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                print('!'*80, file=sys.stderr)
                raise
        return _wrap

    attr = super(cls, self).__getattribute__(attrname)

    if attrname.startswith('test') and callable(attr):
        attr = test_wrap(attr)

    return attr


class TestCase(_TestCase):

    test_name_fout = sys.stderr

    test_name_format = '\n{bar}\nRunning test: {name}\n{bar}\n'

    def setUp(self):
        # Always print the current test name before the test.
        kwargs = dict(
            bar='#'*80,
            name=self._testMethodName,
        )
        print(self.test_name_format.format(**kwargs), file=self.test_name_fout)
        super(TestCase, self).setUp()


class HelperFunctionTests(TestCase):
    """Tests for standalone helper functions."""

    def test_sanitize_index_name(self):
        """Test that index names are properly sanitized for filesystem use."""
        self.assertEqual(_sanitize_index_name('howdou'), 'howdou')
        self.assertEqual(_sanitize_index_name('my-index'), 'my-index')
        self.assertEqual(_sanitize_index_name('my_index'), 'my_index')
        self.assertEqual(_sanitize_index_name('my index'), 'my_index')
        self.assertEqual(_sanitize_index_name('my/index'), 'my_index')
        self.assertEqual(_sanitize_index_name(''), 'howdou')
        self.assertEqual(_sanitize_index_name(None), 'howdou')
        self.assertEqual(_sanitize_index_name('...'), 'howdou')
        self.assertEqual(_sanitize_index_name('___'), 'howdou')

    def test_build_fts_query_exact(self):
        """Test FTS query building with AND operator (exact mode)."""
        # Single term
        self.assertEqual(_build_fts_query('python', exact=True), '"python"')
        # Multiple terms with AND
        self.assertEqual(_build_fts_query('python list', exact=True), '"python" AND "list"')
        # Special characters stripped
        self.assertEqual(_build_fts_query('python: list-dict', exact=True), '"python" AND "list" AND "dict"')
        # Empty query
        self.assertEqual(_build_fts_query('', exact=True), '')
        self.assertEqual(_build_fts_query(None, exact=True), '')

    def test_build_fts_query_fuzzy(self):
        """Test FTS query building with OR operator (fuzzy mode)."""
        self.assertEqual(_build_fts_query('python list', exact=False), '"python" OR "list"')

    def test_rank_to_score(self):
        """Test conversion of FTS rank to score."""
        # Lower rank should give higher score
        score_0 = _rank_to_score(0)
        score_1 = _rank_to_score(1)
        score_10 = _rank_to_score(10)
        self.assertGreater(score_0, score_1)
        self.assertGreater(score_1, score_10)
        # Specific values
        self.assertEqual(_rank_to_score(0), 100.0)
        self.assertEqual(_rank_to_score(99), 1.0)

    def test_compute_file_hash(self):
        """Test file hash computation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('test content')
            temp_path = f.name
        try:
            hash1 = _compute_file_hash(temp_path)
            self.assertEqual(len(hash1), 64)  # SHA256 hex length

            # Same content should give same hash
            hash2 = _compute_file_hash(temp_path)
            self.assertEqual(hash1, hash2)

            # Different content should give different hash
            with open(temp_path, 'w') as f:
                f.write('different content')
            hash3 = _compute_file_hash(temp_path)
            self.assertNotEqual(hash1, hash3)
        finally:
            os.unlink(temp_path)

    def test_build_entry_id(self):
        """Test entry ID generation."""
        answer = {'text': 'answer text', 'weight': 1, 'date': '2020-01-01'}
        id1 = _build_entry_id('file.yml', ['question1'], answer)
        self.assertEqual(len(id1), 128)  # SHA512 hex length

        # Same inputs should give same ID
        id2 = _build_entry_id('file.yml', ['question1'], answer)
        self.assertEqual(id1, id2)

        # Different question should give different ID
        id3 = _build_entry_id('file.yml', ['question2'], answer)
        self.assertNotEqual(id1, id3)

        # Different answer should give different ID
        answer2 = {'text': 'different answer', 'weight': 1, 'date': '2020-01-01'}
        id4 = _build_entry_id('file.yml', ['question1'], answer2)
        self.assertNotEqual(id1, id4)


class HowdouTestCase(TestCase):

    def call_howdou(self, query):
        parser = get_parser()
        args = vars(parser.parse_args(query.split(' ')))
        ret = HowDoU(**args).run()
        return ret

    def setUp(self):
        super(HowdouTestCase, self).setUp()

        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp(prefix='howdou_test_')

        # Define temporary locations for all persistent data files
        # so we don't corrupt any production system.
        howdou.KNOWLEDGEBASE_INDEX = 'howdou-test'
        howdou.KNOWLEDGEBASE_FN = os.path.join(self.test_dir, '.howdou.yml')
        howdou.KNOWLEDGEBASE_TIMESTAMP_FN = os.path.join(self.test_dir, '.howdou_last')
        howdou.LOCKFILE_PATH = os.path.join(self.test_dir, '.howdou_lock')
        howdou.APP_DATA_DIR = os.path.join(self.test_dir, '.howdou')

        # Create a stub howdou objects for reference.
        parser = get_parser()
        args = vars(parser.parse_args([' ']))
        self.howdou = HowDoU(**args)
        # Purge the local index to ensure we're starting fresh.
        self.howdou.delete_index()

    def tearDown(self):
        # Clean up temporary directory
        if hasattr(self, 'test_dir') and os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_find_true_link(self):
        s = '/url?q=http://stackoverflow.com/questions/11004721/how-to-do-i-convert-an-animated-gif-to-an-mp4-or-mv4-on-the-command-line&sa=U'
        ret = howdou.find_true_link(s)
        self.assertEqual(ret, 'http://stackoverflow.com/questions/11004721/how-to-do-i-convert-an-animated-gif-to-an-mp4-or-mv4-on-the-command-line&sa=U')

    def test_get_link_at_pos(self):
        self.assertEqual(howdou.get_link_at_pos(['/questions/42/'], 1), '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/questions/42/'], 2), '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/howdou', '/questions/42/'], 1), '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/howdou', '/questions/42/'], 2), '/questions/42/')
        self.assertEqual(howdou.get_link_at_pos(['/questions/42/', '/questions/142/'], 1), '/questions/42/')

    def test_local_cache_index(self):
        """Test basic local indexing and search functionality."""
        # Create a seed knowledge base.
        self.howdou.init_kb()
        self.assertTrue(os.path.isfile(howdou.KNOWLEDGEBASE_FN))

        # Confirm there's nothing yet indexed in our knowledge base.
        self.assertFalse(self.howdou.is_indexed(
            'how do I create a new howdou knowledge base entry',
            'nano ~/.howdou.yml\nhowdou --reindex',
        ))

        # Re-index the knowledge base file.
        self.howdou.verbose = True
        self.howdou.reindex()

        # Search the index.
        self.howdou.ignore_local = False
        self.howdou.ignore_remote = True
        ret = self.howdou.ask(q='how do I create a new howdou knowledge base entry', output=False)
        print('ret:')
        pprint(ret, indent=4)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0]['answer'], 'nano ~/.howdou.yml\nhowdou --reindex')

        # Add a new item that should not conflict with the existing one.
        item = yaml.safe_load('''
questions:
-   how many toads can a pickle tickle
tags:
-   context:
answers:
-   weight: 1
    date: 2017-2-1
    source:
    tags:
    formatter: nl
    action_subject: []
    text: |-
        twice as many as a canary
''')
        print('item:', item)
        self.howdou.add_item(item)
        print('kb:', self.howdou.kb_filename)
        print(open(self.howdou.kb_filename).read())
        self.howdou.reindex()
        self.assertEqual(self.howdou.last_reindex_count, 2)

        # Ask the same question as before and ensure the result hasn't changed.
        ret = self.howdou.ask(q='how do I create a new howdou knowledge base entry', output=False)
        print('ret:')
        pprint(ret, indent=4)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0]['answer'], 'nano ~/.howdou.yml\nhowdou --reindex')

        # Ask a new question that should match the new entry and confirm a new result.
        ret = self.howdou.ask(q='how many toads can a pickle tickle', output=False)
        print('ret:')
        pprint(ret, indent=4)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0]['answer'], 'twice as many as a canary')

        # Add a new item that should conflict with an existing one, but still not skew results.
        item = yaml.safe_load('''
questions:
-   how do I delete a howdou knowledge base entry
tags:
-   context:
answers:
-   weight: 1
    date: 2017-2-1
    source:
    tags:
    formatter: nl
    action_subject: []
    text: |-
        1. open .howdou.yml
        2. find entry
        3. delete entry
        4. that's it
''')
        print('item:', item)
        self.howdou.add_item(item)
        self.howdou.reindex()
        self.assertEqual(self.howdou.last_reindex_count, 3)

        # Ask our original question and confirm the original result.
        ret = self.howdou.ask(q='how do I create a new howdou knowledge base entry', output=False)
        print('ret:')
        pprint(ret, indent=4)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0]['answer'], 'nano ~/.howdou.yml\nhowdou --reindex')

        # Ask a question that should find the new entry.
        ret = self.howdou.ask(q='how do I delete a howdou knowledge base entry', output=False)
        print('ret:')
        pprint(ret, indent=4)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0]['answer'], '1. open .howdou.yml\n2. find entry\n3. delete entry\n4. that\'s it')

    def test_incremental_indexing(self):
        """Test that only changed files are re-indexed."""
        # Create initial knowledge base
        self.howdou.init_kb()
        self.howdou.reindex()
        initial_count = self.howdou.last_reindex_count

        # Re-index without changes should report no changes
        self.howdou.force = False
        self.howdou.reindex()
        # Count should be 0 since nothing changed
        self.assertEqual(self.howdou.last_reindex_count, 0)

        # Add a new entry
        item = yaml.safe_load('''
questions:
-   test incremental indexing question
answers:
-   weight: 1
    date: 2020-01-01
    text: test incremental answer
''')
        self.howdou.add_item(item)
        self.howdou.reindex()
        # Should have indexed new entries
        self.assertGreater(self.howdou.last_reindex_count, 0)

    def test_entry_removal(self):
        """Test that removed entries are deleted from the index."""
        # Create knowledge base with two entries (using completely non-overlapping terms)
        kb_content = '''
- questions:
  - apple banana cherry
  answers:
  - weight: 1
    date: 2020-01-01
    text: fruit salad recipe
- questions:
  - xylophone zebra quantum
  answers:
  - weight: 1
    date: 2020-01-01
    text: random words collection
'''
        with open(howdou.KNOWLEDGEBASE_FN, 'w') as f:
            f.write(kb_content)

        self.howdou.reindex()

        # Verify both entries are searchable
        self.howdou.ignore_local = False
        self.howdou.ignore_remote = True
        ret = self.howdou.ask(q='apple banana', output=False)
        self.assertEqual(len(ret), 1)
        ret = self.howdou.ask(q='xylophone zebra', output=False)
        self.assertEqual(len(ret), 1)

        # Remove one entry
        kb_content_updated = '''
- questions:
  - apple banana cherry
  answers:
  - weight: 1
    date: 2020-01-01
    text: fruit salad recipe
'''
        with open(howdou.KNOWLEDGEBASE_FN, 'w') as f:
            f.write(kb_content_updated)

        self.howdou.force = False
        self.howdou.reindex()

        # First entry should still be searchable
        ret = self.howdou.ask(q='apple banana', output=False)
        self.assertEqual(len(ret), 1)

        # Second entry should no longer be found
        ret = self.howdou.ask(q='xylophone zebra', output=False)
        self.assertEqual(len(ret), 0)

    def test_weighted_search(self):
        """Test that weight affects search result ordering."""
        kb_content = '''
- questions:
  - python loop iteration
  answers:
  - weight: 1
    date: 2020-01-01
    text: low weight answer
- questions:
  - python loop through list
  answers:
  - weight: 10
    date: 2020-01-01
    text: high weight answer
'''
        with open(howdou.KNOWLEDGEBASE_FN, 'w') as f:
            f.write(kb_content)

        self.howdou.reindex()
        self.howdou.ignore_local = False
        self.howdou.ignore_remote = True
        self.howdou.num_answers = 2

        ret = self.howdou.ask(q='python loop', output=False)
        self.assertEqual(len(ret), 2)
        # Higher weight should come first
        self.assertEqual(ret[0]['answer'], 'high weight answer')
        self.assertEqual(ret[1]['answer'], 'low weight answer')

    def test_database_creation(self):
        """Test that database is created with correct schema."""
        self.howdou.init_kb()
        self.howdou.reindex()

        # Verify database file exists
        self.assertTrue(os.path.isfile(self.howdou.kb_db_filename))

        # Verify tables exist
        import sqlite3
        conn = sqlite3.connect(self.howdou.kb_db_filename)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        self.assertIn('kb', tables)
        self.assertIn('kb_files', tables)

    def test_force_reindex(self):
        """Test that force flag triggers full reindex."""
        self.howdou.init_kb()
        self.howdou.reindex()
        initial_count = self.howdou.last_reindex_count

        # Without force, no reindex needed
        self.howdou.force = False
        self.howdou.reindex()
        self.assertEqual(self.howdou.last_reindex_count, 0)

        # With force, should reindex everything
        self.howdou.force = True
        self.howdou.reindex()
        self.assertEqual(self.howdou.last_reindex_count, initial_count)

    def test_empty_kb_file(self):
        """Test handling of empty knowledge base file."""
        # Create empty file
        with open(howdou.KNOWLEDGEBASE_FN, 'w') as f:
            f.write('')

        # Should not raise an error
        self.howdou.reindex()
        self.assertEqual(self.howdou.last_reindex_count, 0)

    def test_fuzzy_search(self):
        """Test that partial keyword matches work."""
        kb_content = '''
- questions:
  - how to install docker on ubuntu linux
  answers:
  - weight: 1
    date: 2020-01-01
    text: apt-get install docker.io
'''
        with open(howdou.KNOWLEDGEBASE_FN, 'w') as f:
            f.write(kb_content)

        self.howdou.reindex()
        self.howdou.ignore_local = False
        self.howdou.ignore_remote = True

        # Exact match should work
        ret = self.howdou.ask(q='install docker ubuntu', output=False)
        self.assertEqual(len(ret), 1)

        # Partial match (OR mode) should also find it
        ret = self.howdou.ask(q='docker installation', output=False)
        self.assertEqual(len(ret), 1)


class HowdouTestCaseEnvProxies(TestCase):

    def setUp(self):
        super(HowdouTestCaseEnvProxies, self).setUp()
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
