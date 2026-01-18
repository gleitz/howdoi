#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import datetime
# import glob
import json
import os
import re
import sys
import hashlib
import shutil
import sqlite3
import traceback
from pprint import pprint
try:
    from commands import getoutput
except ImportError:
    from subprocess import getoutput
from collections import defaultdict

#https://pythonhosted.org/six/
from six import text_type, string_types

import requests
#from requests.exceptions import ConnectionError # pylint: disable=redefined-builtin
from requests.exceptions import SSLError

import yaml

import dateutil.parser

from fake_useragent import UserAgent

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter # pylint: disable=no-name-in-module
from pygments.util import ClassNotFound

# import requests_cache

try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

try:
    from urllib import getproxies
except ImportError:
    from urllib.request import getproxies

import fasteners

from pyquery import PyQuery as pq

#from howdou import __version__
from .__init__ import __version__

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

LOCAL = 'local'
REMOTE = 'remote'

KNOWLEDGEBASE_FN = os.path.expanduser(os.getenv('HOWDOU_KB', '~/.howdou.yml'))
KNOWLEDGEBASE_INDEX = os.getenv('HOWDOU_INDEX', 'howdou')
KNOWLEDGEBASE_TIMESTAMP_FN = os.path.expanduser(os.getenv('HOWDOU_TIMESTAMP', '~/.howdou_last'))
APP_DATA_DIR = os.path.expanduser(os.getenv('HOWDOU_DIR', '~/.howdou'))
KNOWLEDGEBASE_DB_FN = os.getenv('HOWDOU_DB')
LOCKFILE_PATH = os.path.expanduser(os.getenv('HOWDOU_LOCKFILE', '~/.howdou_lock'))
CACHE_DIR = os.path.join(os.path.join(os.path.expanduser('~'), '.cache'), 'howdou')

KNOWLEDGEBASE_STUB = '''-   questions:
    -   how do I create a new howdou knowledge base entry
    tags:
        context: howdou
    answers:
    -   weight: 1
        date: 2014-2-22
        source:
        formatter:
        text: |
            nano ~/.howdou.yml
            howdou --reindex
'''

if os.getenv('HOWDOU_DISABLE_SSL'): # Set http instead of https
    SEARCH_URL = 'http://www.google.com/search?q=site:{0}%20{1}'
else:
    SEARCH_URL = 'https://www.google.com/search?q=site:{0}%20{1}'

LOCALIZATION = os.getenv('HOWDOU_LOCALIZATION') or 'en'

LOCALIZATON_URLS = {
    'en': 'stackoverflow.com',
    'pt-br': 'pt.stackoverflow.com',
}

ANSWER_HEADER = u('--- Answer: {i} --- Weight: {weight} --- Source: {source} ---\n\n{answer}')

NO_ANSWER_MSG = '< no answer given >'

QUERY = 'query'
REINDEX = 'reindex'
CLEAR_CACHE = 'clear-cache'
SUMMARIZE_FIELD = 'summarize-field'
FILTER_BY_FIELD = 'filter-by-field'
ACTIONS = (QUERY, REINDEX, CLEAR_CACHE, SUMMARIZE_FIELD, FILTER_BY_FIELD)

DEFAULT_USERAGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'

ua = UserAgent(fallback=DEFAULT_USERAGENT)

# Force dictionaries to be serialized in multi-line format.
def _represent_dictorder(self, data):
    _data = []
    ordering = ['questions', 'tags', 'answers', 'weight', 'date', 'source', 'formatter', 'action_subject', 'text']
    for key in ordering:
        if key in data:
            _data.append((str(key), data.pop(key)))
    if data:
        _data.extend(data.items())
    return self.represent_mapping(u'tag:yaml.org,2002:map', _data)

# def _represent_tuple(self, data):
    # return self.represent_sequence(u'tag:yaml.org,2002:seq', data)

# def _construct_tuple(self, node):
    # return tuple(self.construct_sequence(node))

# def _represent_function(self, data):
    # return self.represent_scalar(u'tag:yaml.org,2002:null', u'null')

def _selective_representer(dumper, data):
    return dumper.represent_scalar(u"tag:yaml.org,2002:str", data, style="|" if "\n" in data else None)

yaml.add_representer(str, _selective_representer)
yaml.add_representer(text_type, _selective_representer)
yaml.add_representer(dict, _represent_dictorder)
# yaml.add_representer(_AliasDict, _represent_dictorder)
#yaml.add_representer(tuple, _represent_tuple) # we need tuples for hash keys
# yaml.add_constructor(u'tag:yaml.org,2002:python/tuple', _construct_tuple)
# yaml.add_representer(types.FunctionType, _represent_function)

def _sanitize_index_name(name):
    """
    Returns a filesystem-safe name suitable for use in a SQLite filename.
    """
    safe = re.sub(r'[^A-Za-z0-9_.-]+', '_', name or '')
    safe = safe.strip('._-')
    return safe or 'howdou'

def _build_fts_query(query, exact=True):
    """
    Builds a conservative FTS5 query string from user input.
    """
    query = re.sub(r'[\:\-]+', ' ', query or '')
    query = re.sub(r'[^\w\s]+', ' ', query, flags=re.UNICODE)
    terms = [term for term in query.split() if term]
    if not terms:
        return ''
    operator = ' AND ' if exact else ' OR '
    return operator.join(['"%s"' % term.replace('"', '""') for term in terms])

def _rank_to_score(rank):
    """
    Converts an FTS bm25 rank (lower is better) into a higher-is-better score.
    """
    return 100.0 / (rank + 1.0)

def _compute_file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fin:
        for chunk in iter(lambda: fin.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def _normalize_action_subject(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [text_type(item) for item in value]
    return [text_type(value)]

def _build_entry_id(filename, questions_list, answer, item_tags=None):
    payload = {
        'filename': filename,
        'questions': [text_type(q) for q in questions_list],
        'answer': text_type(answer.get('text', '')),
        'source': text_type(answer.get('source', '') or ''),
        'weight': float(answer.get('weight', 1)),
        'date': text_type(answer.get('date', '') or ''),
        'formatter': text_type(answer.get('formatter', '') or ''),
        'action_subject': _normalize_action_subject(answer.get('action_subject')),
        'answer_tags': answer.get('tags'),
        'entry_tags': item_tags,
    }
    payload_str = json.dumps(payload, sort_keys=True, default=text_type)
    return get_text_hash(payload_str)

def get_nested_key(element, keys):
    """
    Returns the key at the nested position inside element, which should be a nested dictionary.
    """
    keys = list(keys)
    if not keys:
        return element
    key = keys.pop(0)
    if key not in element:
        return
    return get_nested_key(element[key], keys)

def get_link_at_pos(links, position):

    def is_question(link):
        return re.search(r'questions/\d+/', link)

    links = [link for link in links if is_question(link)]
    if not links:
        return False

    if len(links) >= position:
        link = links[position-1]
    else:
        link = links[-1]
    return link

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def get_text_hash(text):
    """
    Returns the hash of the given text.
    """
    h = hashlib.sha512()
    if not isinstance(text, text_type):
        text = text_type(text, encoding='utf-8', errors='replace')
    h.update(text.encode('utf-8', 'replace'))
    return h.hexdigest()

def get_proxies():
    proxies = getproxies()
    filtered_proxies = {}
    for key, value in proxies.items():
        if key.startswith('http'):
            if not value.startswith('http'):
                filtered_proxies[key] = 'http://%s' % value
            else:
                filtered_proxies[key] = value
    return filtered_proxies

def find_true_link(s):
    """
    Sometimes Google wraps our links inside sneaky tracking links, which often fail and slow us down
    so remove them.
    """
    # Convert "/url?q=<real_url>" to "<real_url>".
    if s and s.startswith('/') and 'http' in s:
        s = s[s.find('http'):]
    return s

class HowDoU():

    def __init__(self, **kwargs):
        kwargs.setdefault('verbose', False)
        self.__dict__.update(kwargs)

        if self.verbose:
            print('kwargs:')
            pprint(kwargs, indent=4)
        assert self.action in ACTIONS, 'Invalid action "%s". Must be one of %s' % (self.action, ', '.join(ACTIONS))

        self.cache_file = os.path.join(self.cache_dir, 'cache')

        self.query = (' '.join(self.query).replace('?', '')).strip()

        self.kb_filename = os.path.expanduser(self.kb_filename)
        self.kb_timestamp = os.path.expanduser(self.kb_timestamp)
        self.kb_app_dir = os.path.expanduser(self.kb_app_dir)
        if self.kb_db_filename:
            self.kb_db_filename = os.path.expanduser(self.kb_db_filename)
        else:
            safe_index = _sanitize_index_name(self.kb_index_name)
            self.kb_db_filename = os.path.join(self.kb_app_dir, '%s.db' % safe_index)

        self.append_header = False

        self.last_reindex_count = 0

    def _ensure_db(self):
        if not os.path.isdir(self.kb_app_dir):
            os.makedirs(self.kb_app_dir)
        conn = sqlite3.connect(self.kb_db_filename)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS kb_files ("
                "filename TEXT PRIMARY KEY, "
                "file_hash TEXT NOT NULL, "
                "updated_at TEXT NOT NULL)"
            )
            columns = [row['name'] for row in conn.execute("PRAGMA table_info(kb)").fetchall()]
            if not columns:
                conn.execute(
                    "CREATE VIRTUAL TABLE kb USING fts5("
                    "entry_id UNINDEXED, "
                    "questions, "
                    "answer UNINDEXED, "
                    "source UNINDEXED, "
                    "filename UNINDEXED, "
                    "text UNINDEXED, "
                    "action_subject UNINDEXED, "
                    "timestamp UNINDEXED, "
                    "weight UNINDEXED)"
                )
            elif 'entry_id' not in columns:
                conn.execute("DROP TABLE IF EXISTS kb")
                conn.execute("DELETE FROM kb_files")
                conn.execute(
                    "CREATE VIRTUAL TABLE kb USING fts5("
                    "entry_id UNINDEXED, "
                    "questions, "
                    "answer UNINDEXED, "
                    "source UNINDEXED, "
                    "filename UNINDEXED, "
                    "text UNINDEXED, "
                    "action_subject UNINDEXED, "
                    "timestamp UNINDEXED, "
                    "weight UNINDEXED)"
                )
        except sqlite3.OperationalError as exc:
            conn.close()
            if 'fts5' in str(exc).lower():
                raise RuntimeError('SQLite FTS5 support is required for local search.') from exc
            raise
        return conn

    def _clear_kb_cache(self):
        if not os.path.isdir(self.kb_app_dir):
            return
        for entry in os.listdir(self.kb_app_dir):
            path = os.path.join(self.kb_app_dir, entry)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except OSError:
                pass

    def delete_index(self):
        """
        Forcibly deletes the local index.
        """
        print('Deleting index %s...' % self.kb_index_name)
        if self.kb_db_filename and os.path.isfile(self.kb_db_filename):
            try:
                os.remove(self.kb_db_filename)
            except OSError:
                pass
        print('Deleting index cache at %s...' % self.kb_app_dir)
        self._clear_kb_cache()

    def is_kb_updated(self):
        """
        Returns true if any knowledge base file has changed since the last run.
        """
        conn = self._ensure_db()
        try:
            kb_filenames = self.list_kb_files()
            stored_filenames = set(
                row['filename'] for row in conn.execute("SELECT filename FROM kb_files").fetchall()
            )
            if set(kb_filenames) != stored_filenames:
                print('Changes found.')
                return True
            for kb_filename in kb_filenames:
                current_hash = _compute_file_hash(kb_filename)
                row = conn.execute(
                    "SELECT file_hash FROM kb_files WHERE filename = ?",
                    (kb_filename,),
                ).fetchone()
                if not row or row['file_hash'] != current_hash:
                    print('Changes found.')
                    return True
        finally:
            conn.close()
        return False

    def update_kb_timestamp(self):
        touch(self.kb_timestamp)

    def get_result(self, url):
        try:
            return requests.get(url, headers={'User-Agent': ua.random}, proxies=get_proxies()).text
        except SSLError as e:
            print('[ERROR] Encountered an SSL Error. Try using HTTP instead of '
                  'HTTPS by setting the environment variable "HOWDOU_DISABLE_SSL".\n')
            raise e

    def get_links(self, query):
        localization_url = LOCALIZATON_URLS[self.lang]
        result = self.get_result(SEARCH_URL.format(localization_url, url_quote(query)))
        html = pq(result)
        return [a.attrib['href'] for a in html('.l')] or [a.attrib['href'] for a in html('.r')('a')]

    def format_output(self, code):
        if not self.color:
            return code
        lexer = None

        # try to find a lexer using the StackOverflow tags
        # or the query arguments
        for keyword in self.query.split() + self.tags:
            try:
                lexer = get_lexer_by_name(keyword)
                break
            except ClassNotFound:
                pass

        # no lexer found above, use the guesser
        if not lexer:
            lexer = guess_lexer(code)

        return highlight(code, lexer, TerminalFormatter(bg='dark'))

    def get_answer(self, links):
        """
        Given search arguments and a links of web links (usually Stackoverflow),
        find the best answer to the search question.
        """
        #print('get_answer: args:', args, 'links:', links)
        link = get_link_at_pos(links, self.pos)
        if not link:
            return False, None

        # Don't lookup answer text, just return link.
        if self.link:
            return None, link

        page = self.get_result(find_true_link(link) + '?answertab=votes')
        html = pq(page)

        first_answer = html('.answer').eq(0)
        instructions = first_answer.find('pre') or first_answer.find('code')
        self.tags = [t.text for t in html('.post-tag')]

        if not instructions and not self.all:
            text = first_answer.find('.post-text').eq(0).text()
        elif self.all:
            texts = []
            for html_tag in first_answer.items('.post-text > *'):
                current_text = html_tag.text()
                if current_text:
                    if html_tag[0].tag in ['pre', 'code']:
                        texts.append(self.format_output(current_text))
                    else:
                        texts.append(current_text)
            texts.append('\n---\nAnswer from {0}'.format(link))
            text = '\n'.join(texts)
        else:
            text = self.format_output(instructions.eq(0).text())
        if text is None:
            text = NO_ANSWER_MSG
        text = text.strip()
        return text, link

    def run_clear_cache(self):
        self.clear_cache()

    def clear_cache(self):
        self.delete_index()

    def init_kb(self):
        if not os.path.isfile(self.kb_filename):
            with open(self.kb_filename, 'w') as fout:
                fout.write(KNOWLEDGEBASE_STUB)

    def mark_indexed(self, question_str, answer_str):
        hash_fn = os.path.join(self.kb_app_dir, get_text_hash(question_str))
        hash_contents = get_text_hash(answer_str)
        open(hash_fn, 'w').write(hash_contents)

    def is_indexed(self, question_str, answer_str):
        """
        Returns true if this exact combination has been previously indexed.
        Returns false otherwise.
        """
        hash_fn = os.path.join(self.kb_app_dir, get_text_hash(question_str))
        if not os.path.isfile(hash_fn):
            return False
        hash_contents = get_text_hash(answer_str)
        if open(hash_fn).read() != hash_contents:
            return False
        return True

    def add_item(self, item):
        """
        Dynamically appends an item to the knowledge base.
        Warning, this will overwrite the file!
        """
        assert isinstance(item, dict)
        assert 'questions' in item
        assert 'answers' in item and item['answers']
        for answer in item['answers']:
            assert 'date' in answer
            assert 'text' in answer
            answer.setdefault('weight', 1.0)
        item_str = yaml.dump([item], indent=4, default_flow_style=False)#, default_style='|')
        self.init_kb()
        with open(self.kb_filename, 'a') as fout:
            fout.write(item_str)

    def show_gui_error(self, message, detail):
        getoutput('export DISPLAY=:0; notify-send "%s" "%s"' % (message, detail))

    def count_total_kb_entries(self, fn=None):
        cnt = 0
        for item in self.iter_kb(fn=None):
            cnt += 1
        return cnt

    def count_total_kb_answers(self, fn=None):
        cnt = 0
        for item in self.iter_kb(fn=None):
            if 'answers' in item:
                cnt += len(item['answers'])
        return cnt

    def iter_kb(self, fn=None, only_filenames=False):
        """
        Iterates over all knowledgebase entries.
        """
        if not os.path.isdir(self.kb_app_dir):
            os.mkdir(self.kb_app_dir)
        if only_filenames and fn is None:
            yield self.kb_filename
        fn = fn or self.kb_filename
        try:
            with open(fn) as fin:
                items = yaml.load(fin, Loader=yaml.FullLoader)
            if not items:
                return
            for item in items:
                if isinstance(item, dict) and 'include' in item:
                    # Handle special "include" entries that direct us to load an additional file.
                    if only_filenames:
                        yield item['include']
                    else:
                        for _ in self.iter_kb(item['include']):
                            yield _
                else:
                    # Otherwise, yield normal entry.
                    # Dynamically add filename so it can be indexed and included in search results.
                    item['filename'] = fn
                    yield item
        except TypeError:
            return

    def iter_kb_file(self, fn):
        """
        Iterates over entries in a single knowledge base file, ignoring include directives.
        """
        try:
            with open(fn) as fin:
                items = yaml.load(fin, Loader=yaml.FullLoader)
            if not items:
                return
            for item in items:
                if isinstance(item, dict) and 'include' in item:
                    continue
                if isinstance(item, dict):
                    item['filename'] = fn
                    yield item
        except TypeError:
            return

    def list_kb_files(self):
        kb_filenames = []
        seen = set()

        def _add_file(path):
            if not path or path in seen:
                return
            seen.add(path)
            kb_filenames.append(path)
            try:
                with open(path) as fin:
                    items = yaml.load(fin, Loader=yaml.FullLoader)
            except TypeError:
                return
            if not items:
                return
            for item in items:
                if isinstance(item, dict) and 'include' in item:
                    _add_file(item['include'])

        _add_file(self.kb_filename)
        return kb_filenames

    def index_kb(self):
        """
        Processes all knowledgebase entries and enters them into the text search database.
        """
        count = 0

        if self.force:
            self.delete_index()
        conn = self._ensure_db()
        try:
            try:
                kb_filenames = self.list_kb_files()
            except yaml.scanner.ScannerError as exc:
                traceback.print_exc()
                self.show_gui_error('HowDoU Re-Indexing Error', exc)
                sys.exit(1)
            stored_filenames = set(
                row['filename'] for row in conn.execute("SELECT filename FROM kb_files").fetchall()
            )
            current_filenames = set(kb_filenames)
            removed_filenames = stored_filenames - current_filenames

            file_hashes = {}
            changed_filenames = []
            for kb_filename in kb_filenames:
                current_hash = _compute_file_hash(kb_filename)
                file_hashes[kb_filename] = current_hash
                row = conn.execute(
                    "SELECT file_hash FROM kb_files WHERE filename = ?",
                    (kb_filename,),
                ).fetchone()
                if self.force or row is None or row['file_hash'] != current_hash:
                    changed_filenames.append(kb_filename)

            if not self.force and not changed_filenames and not removed_filenames:
                print('No changes detected.')
                self.last_reindex_count = 0
                return

            for kb_filename in removed_filenames:
                conn.execute("DELETE FROM kb WHERE filename = ?", (kb_filename,))
                conn.execute("DELETE FROM kb_files WHERE filename = ?", (kb_filename,))

            # Count total combinations so we can accurately measure progress.
            self.vprint('kb_filename:', self.kb_filename)
            total = 0
            try:
                for kb_filename in changed_filenames:
                    for item in self.iter_kb_file(kb_filename):
                        if 'answers' in item:
                            total += len(item['answers'])
            except yaml.scanner.ScannerError as exc:
                traceback.print_exc()
                self.show_gui_error('HowDoU Re-Indexing Error', exc)
                sys.exit(1)

            for kb_filename in changed_filenames:
                existing_entry_ids = set(
                    row['entry_id'] for row in conn.execute(
                        "SELECT entry_id FROM kb WHERE filename = ?",
                        (kb_filename,),
                    ).fetchall()
                )
                current_entries = {}

                for item in self.iter_kb_file(kb_filename):
                    # Combine the list of separate questions into a single text block.
                    print('item:', item)
                    questions_list = item.get('questions') or []
                    questions = u'\n'.join(map(text_type, questions_list))
                    self.vprint('questions:', questions)
                    if not questions:
                        print('Skipping due to missing questions.')
                        continue
                    answers = item.get('answers') or []
                    if not answers:
                        continue

                    for answer in answers:
                        count += 1
                        sys.stdout.write('\rRe-indexing %i of %i...' % (count, total))
                        sys.stdout.flush()

                        weight = float(answer.get('weight', 1))
                        dt = answer['date']
                        if isinstance(dt, string_types):
                            try:
                                dt = dateutil.parser.parse(dt)
                            except ValueError as e:
                                raise Exception('Invalid date: %s' % dt)

                        text = questions + ' ' + answer['text']
                        entry_id = _build_entry_id(
                            kb_filename, questions_list, answer, item_tags=item.get('tags')
                        )

                        doc = dict(
                            entry_id=entry_id,
                            questions=questions,
                            answer=answer['text'],
                            source=answer.get('source', ''),
                            filename=item['filename'],
                            text=text,
                            action_subject=answer.get('action_subject'),
                            timestamp=dt,
                            weight=weight,
                        )
                        if self.verbose:
                            print('doc:')
                            pprint(doc, indent=4)

                        current_entries[entry_id] = doc

                current_entry_ids = set(current_entries.keys())
                to_remove = existing_entry_ids - current_entry_ids
                to_add = current_entry_ids - existing_entry_ids

                if to_remove:
                    placeholders = ','.join(['?'] * len(to_remove))
                    # FTS5 requires explicit rowid for DELETE
                    cursor = conn.execute(
                        "SELECT rowid FROM kb WHERE filename = ? AND entry_id IN (%s)" % placeholders,
                        (kb_filename,) + tuple(to_remove),
                    )
                    rowids_to_delete = [row[0] for row in cursor.fetchall()]
                    for rowid in rowids_to_delete:
                        conn.execute("DELETE FROM kb WHERE rowid = ?", (rowid,))

                for entry_id in to_add:
                    doc = current_entries[entry_id]
                    # Register this combination in the database.
                    action_subject = doc['action_subject']
                    if isinstance(action_subject, (list, tuple)):
                        action_subject = ','.join(map(text_type, action_subject))
                    elif action_subject is None:
                        action_subject = ''
                    else:
                        action_subject = text_type(action_subject)
                    timestamp = doc['timestamp']
                    if isinstance(timestamp, datetime.datetime):
                        timestamp = timestamp.isoformat()
                    else:
                        timestamp = text_type(timestamp)
                    conn.execute(
                        "INSERT INTO kb "
                        "(entry_id, questions, answer, source, filename, text, action_subject, timestamp, weight) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            doc['entry_id'],
                            doc['questions'],
                            doc['answer'],
                            doc['source'],
                            doc['filename'],
                            doc['text'],
                            action_subject,
                            timestamp,
                            text_type(doc['weight']),
                        ),
                    )

                conn.execute(
                    "INSERT OR REPLACE INTO kb_files (filename, file_hash, updated_at) "
                    "VALUES (?, ?, ?)",
                    (
                        kb_filename,
                        file_hashes[kb_filename],
                        datetime.datetime.utcnow().isoformat(),
                    ),
                )

            self.last_reindex_count = count
            conn.commit()
        finally:
            conn.close()
        self.update_kb_timestamp()
        print('\nRe-indexed %i items.' % (count,))

    def vprint(self, *args):
        if self.verbose:
            print(' '.join(map(str, args)))
            sys.stdout.flush()

    def get_local_answers(self, q=None):

        def _get_search_results(exact=True):
            fts_query = _build_fts_query(query, exact=exact)
            if not fts_query:
                return []
            sql = (
                "SELECT questions, answer, source, filename, text, weight, "
                "(bm25(kb) * CASE WHEN CAST(weight AS REAL) > 0 "
                "THEN CAST(weight AS REAL) ELSE 1 END) AS rank "
                "FROM kb "
                "WHERE kb MATCH ? "
                "ORDER BY rank "
                "LIMIT ?"
            )
            return conn.execute(sql, (fts_query, self.num_answers)).fetchall()

        query = q or self.query
        assert query and isinstance(query, string_types), 'Invalid query: %s' % query
        answers = []
        conn = self._ensure_db()
        self.vprint('Checking for local answers at index %s...' % self.kb_index_name)

        try:
            for method in [lambda: _get_search_results(exact=True), lambda: _get_search_results(exact=False)]:
                rows = method()
                total = len(rows)
                self.vprint('Found %i results.' % total)
                if self.verbose:
                    print('rows:')
                    pprint([dict(row) for row in rows], indent=4)
                if rows:
                    for row in rows:
                        answer_data = {}
                        score = _rank_to_score(row['rank'] or 0.0)
                        if self.min_score >= 0 and score < self.min_score:
                            continue

                        answer_data['answer'] = (row['answer'] or '').strip()
                        answer_data['score'] = score
                        answer_data['source'] = (row['source'] or '').strip() or None
                        _fn = row['filename']
                        answer_data['filename'] = _fn
                        answer_data['text'] = row['text']
                        answer_data['weight'] = float(row['weight'] or 0.0)
                        answer_data['location'] = LOCAL
                        if self.verbose:
                            print('answer_data:')
                            pprint(answer_data, indent=4)
                        answers.append(answer_data)

                # First try finding an entry with all the keywords using the AND operator.
                # If nothing found, then continue by searching for entries with any of the keywords
                # using the OR operator.
                if total:
                    break
        finally:
            conn.close()

        return answers

    def reindex(self, *args, **kwargs):
        return self.run_reindex(*args, **kwargs)

    def ask(self, *args, **kwargs):
        return self.run_query(*args, **kwargs)

    def run_query(self, q=None, output=True):
        query = q or self.query

        # SQLite FTS tokenizes text on certain non-alphanumeric characters,
        # so increase a query's chances of finding an exact match by removing these tokens.
        query = re.sub(r'[\:\-]+', ' ', query)

        answers = []
        if query:
            with fasteners.InterProcessLock(self.kb_lockfile_path):

                self.init_kb()

                # enable the cache if user doesn't want it to be disabled
                # if not self.disable_cache:
                    # self.enable_cache()

                self.append_header = self.num_answers > 1 or self.show_score or self.show_source
                #initial_position = self.pos

                self.vprint('Querying %s...' % query)

                # Check local index first.
                if not self.ignore_local:
                    answers.extend(self.get_local_answers(query))

                # If we found nothing satisfying locally, then search the net.
                if not answers and not self.ignore_remote:
                    links = self.get_links(query)
                    if not links:
                        return False
                    for answer_number in range(self.num_answers):
                        result = self.get_answer(links)
                        answer, link = result
                        if not answer and not link:
                            continue

                        answer_data = {}
                        answer_data['answer'] = answer
                        answer_data['score'] = 1.0
                        answer_data['source'] = link
                        answer_data['filename'] = None
                        answer_data['text'] = None
                        answer_data['weight'] = 1.0
                        answer_data['location'] = REMOTE
                        answers.append(answer_data)

        if output:
            s = []
            for i, answer in enumerate(answers):
                if answer['location'] == LOCAL:
                    source = answer['filename']
                else:
                    source = answer['source']
                score = int(round(answer['score'] or 0, 0))
                weight = int(answer['weight'] or 0)
                s.append(ANSWER_HEADER.format(
                    i=i+1,
                    weight=score*weight,
                    answer=answer['answer'],
                    source=source))

            output_str = u'\n' + (u'\n\n'.join(s)) + u'\n'
            output_str.encode('utf-8', 'replace')
            try:
                # Try to print unicode.
                print(output_str)
            except UnicodeEncodeError:
                # If the console forces us to use ASCII, then force ASCII.
                print(output_str.encode('ascii', 'replace'))
            return output_str

        return answers

    def run_reindex(self):
        with fasteners.InterProcessLock(self.kb_lockfile_path):
            self.index_kb()

    def run_summarize_field(self):
        """
        Iterates over all knowledgebase items and counts the values associated with the given field path.
        """
        path = [_.strip() for _ in self.query.split('.') if _.strip()]
        assert path, 'No query path specified.'
        self.vprint('Searching path:', path)
        counts = defaultdict(int)
        for item in self.iter_kb():
            value = get_nested_key(item, path)
            counts[value] += 1
        for v, cnt in sorted(counts.items(), key=lambda o: o[1]):
            print(cnt, v)

    def run_filter_by_field(self):
        """
        Iterates over all knowledgebase items and prints those that correspond to the given field path.
        """
        path, target = self.query.split(' ')
        path = [_.strip() for _ in path.split('.') if _.strip()]
        assert path, 'No query path specified.'
        self.vprint('Searching path:', path)
        self.vprint('Target:', target)
        data = []
        for item in self.iter_kb():
            value = str(get_nested_key(item, path))
            if value != target:
                continue
            if 'answers' in item:
                for answer in item['answers']:
                    answer['text'] = answer['text'].encode('ascii', 'replace')
                    answer['text'] = re.sub(r'\n[\t\s]+\n', '\n\n', answer['text'], flags=re.M)
                    answer['text'] = re.sub(r'(?<=[^\n\t\s])[ ]+(?=$)', '', answer['text'], flags=re.M)
                    answer['text'] = answer['text'].strip() + '\n\n'
            data.append(item)
        yaml.dump(data, stream=sys.stdout, default_flow_style=False, indent=4)

    def run(self):
        run_func = 'run_%s' % self.action.replace('-', '_')
        if hasattr(self, run_func):
            return getattr(self, run_func)()
        raise AttributeError('Invalid action: %s' % self.action)


def get_parser():
    parser = argparse.ArgumentParser(description='instant coding answers via the command line')

    # General purpose options.
    parser.add_argument(
        '-v', '--version',
        help='Show version.',
        action='version',
        version=__version__,
    )
    parser.add_argument(
        '--verbose',
        help='If given, provides excessive output.',
        default=False,
        action='store_true')
    parser.add_argument(
        '--kb-filename',
        help='The knowledge base filename.',
        default=KNOWLEDGEBASE_FN)
    parser.add_argument(
        '--kb-index-name',
        help='The knowledge base index name used for local SQLite storage.',
        default=KNOWLEDGEBASE_INDEX)
    parser.add_argument(
        '--kb-timestamp',
        help='The filename to use to tracking timestamps.',
        default=KNOWLEDGEBASE_TIMESTAMP_FN)
    parser.add_argument(
        '--kb-app-dir',
        help='The filename to use to tracking timestamps.',
        default=APP_DATA_DIR)
    parser.add_argument(
        '--kb-db',
        help='The SQLite database filename used for the local index.',
        default=KNOWLEDGEBASE_DB_FN,
        dest='kb_db_filename')
    parser.add_argument(
        '--kb-lockfile-path',
        help='The filename to use when locking access during updates.',
        default=LOCKFILE_PATH)
    parser.add_argument(
        '--cache-dir',
        help='The filename to use when caching web requests.',
        default=CACHE_DIR)
    parser.add_argument(
        '--lang',
        help='The localization to use. Default is %s.' % LOCALIZATION,
        default=LOCALIZATION)

    # This controls the core behavior initiated from the command line.
    parser.add_argument(
        '--action',
        help='Action to perform. One of %s' % ('|'.join(ACTIONS)),
        default=QUERY)

    # Query action options.
    parser.add_argument(
        'query', metavar='QUERY', type=str, nargs='*',
        help='The question to answer or keywords to search by. Used with the query action.')
    parser.add_argument(
        '-p', '--pos',
        help='select answer in specified position (default: 1)',
        default=1, type=int)
    parser.add_argument(
        '-a', '--all', help='display the full text of the answer',
        action='store_true')
    parser.add_argument(
        '-l', '--link', help='display only the answer link',
        action='store_true')
    parser.add_argument(
        '-c', '--color', help='enable colorized output',
        action='store_true')
    parser.add_argument(
        '-n', '--num-answers',
        help='number of answers to return',
        default=1, type=int)
    parser.add_argument(
        '--min-score',
        help='the minimum score accepted on local answers',
        default=-1, type=float)
    parser.add_argument(
        '--ignore-local',
        help='ignore local cache',
        default=False,
        action='store_true')
    parser.add_argument(
        '--ignore-remote',
        help='ignore remote',
        default=False,
        action='store_true')
    parser.add_argument(
        '--show-score',
        help='display score of all results',
        default=False,
        action='store_true')
    parser.add_argument(
        '--hide-source',
        help='displays any source linked to the answer',
        dest='show_source',
        default=True,
        action='store_false')
    # parser.add_argument(
        # '--disable-cache',
        # help='Disables cache of web requests.',
        # default=bool(os.getenv('HOWDOU_DISABLE_CACHE')),
        # action='store_true')

    # Reindex action options.
    parser.add_argument(
        '--force',
        help='Used with the reindex option, forces reindexing of all items even if no change was made',
        default=False,
        action='store_true')

    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    howdou = HowDoU(**args)
    howdou.run()

if __name__ == '__main__':
    command_line_runner()
