#!/usr/bin/env python

######################################################
#
# howdoi - instant coding answers via the command line
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
######################################################

from __future__ import print_function
import gc
gc.disable()  # noqa: E402
import argparse
import os
import appdirs
import json
import requests
import sys
from . import __version__

from cachelib import FileSystemCache, NullCache

from requests.exceptions import ConnectionError
from requests.exceptions import SSLError

from howdoi.plugins import BasePlugin

CACHE_EMPTY_VAL = "NULL"
CACHE_DIR = appdirs.user_cache_dir('howdoi')
CACHE_ENTRY_MAX = 128

# rudimentary standardized 3-level log output
def _print_err(x): print("[ERROR] " + x)


_print_ok = print  # noqa: E305
def _print_dbg(x): print("[DEBUG] " + x)  # noqa: E302

SUPPORTED_SEARCH_ENGINES = ('google', 'bing', 'duckduckgo')

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
                'Chrome/19.0.1084.46 Safari/536.5'),
               ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
                'Safari/536.5'), )

SUPPORTED_HELP_QUERIES = ['use howdoi', 'howdoi', 'run howdoi',
                          'do howdoi', 'howdoi howdoi', 'howdoi use howdoi']

howdoi_session = requests.session()

if os.getenv('HOWDOI_DISABLE_CACHE'):
    cache = NullCache()  # works like an always empty cache
else:
    cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)


def _random_int(width):
    bres = os.urandom(width)
    if sys.version < '3':
        ires = int(bres.encode('hex'), 16)
    else:
        ires = int.from_bytes(bres, 'little')

    return ires


def _random_choice(seq):
    return seq[_random_int(1) % len(seq)]


def build_splitter(splitter_character='=', splitter_length=80):
    return '\n' + splitter_character * splitter_length + '\n\n'


def _clear_cache():
    global cache
    if not cache:
        cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, 0)

    return cache.clear()


def _is_help_query(query: str):
    return any([query.lower() == help_query for help_query in SUPPORTED_HELP_QUERIES])


def _format_answers(res, args):
    if "error" in res:
        return res["error"]

    if args["json_output"]:
        return json.dumps(res)

    formatted_answers = []

    for answer in res:
        next_ans = answer["answer"]
        if args["link"]:  # if we only want links
            next_ans = answer["link"]
        formatted_answers.append(next_ans)

    return build_splitter().join(formatted_answers)


def _get_help_instructions():
    instruction_splitter = build_splitter(' ', 60)
    query = 'print hello world in python'
    instructions = [
        'Here are a few popular howdoi commands ',
        '>>> howdoi {} (default query)',
        '>>> howdoi {} -a (read entire answer)',
        '>>> howdoi {} -n [number] (retrieve n number of answers)',
        '>>> howdoi {} -l (display only a link to where the answer is from',
        '>>> howdoi {} -c (Add colors to the output)',
        '>>> howdoi {} -e (Specify the search engine you want to use e.g google,bing)'
    ]

    instructions = map(lambda s: s.format(query), instructions)

    return instruction_splitter.join(instructions)


def _get_cache_key(args):
    return str(args) + __version__


def howdoi(raw_query):
    args = raw_query
    if type(raw_query) is str:  # you can pass either a raw or a parsed query
        parser = get_parser()
        args = vars(parser.parse_args(raw_query.split(' ')))

    args['query'] = ' '.join(args['query']).replace('?', '')
    cache_key = _get_cache_key(args)

    if _is_help_query(args['query']):
        return _get_help_instructions() + '\n'

    res = cache.get(cache_key)

    if res:
        return _format_answers(res, args)

    try:
        plugin = BasePlugin.BasePlugin()
        res = plugin.search()
        if not res:
            res = {"error": "Sorry, couldn\'t find any help with that topic\n"}
        cache.set(cache_key, res)
    except (ConnectionError, SSLError):
        return {"error": "Failed to establish network connection\n"}
    finally:
        return _format_answers(res, args)


def get_parser():
    parser = argparse.ArgumentParser(description='instant coding answers via the command line')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*', help='the question to answer')
    parser.add_argument('-p', '--pos', help='select answer in specified position (default: 1)', default=1, type=int)
    parser.add_argument('-a', '--all', help='display the full text of the answer', action='store_true')
    parser.add_argument('-l', '--link', help='display only the answer link', action='store_true')
    parser.add_argument('-c', '--color', help='enable colorized output', action='store_true')
    parser.add_argument('-n', '--num-answers', help='number of answers to return', default=1, type=int)
    parser.add_argument('-C', '--clear-cache', help='clear the cache',
                        action='store_true')
    parser.add_argument('-j', '--json-output', help='return answers in raw json format',
                        action='store_true')
    parser.add_argument('-v', '--version', help='displays the current version of howdoi',
                        action='store_true')
    parser.add_argument('-e', '--engine', help='change search engine for this query only (google, bing, duckduckgo)',
                        dest='search_engine', nargs="?", default='google')
    parser.add_argument('--plugin', help='use the base plugin', type=str, default='stackoverflow')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        _print_ok(__version__)
        return

    if args['clear_cache']:
        if _clear_cache():
            _print_ok('Cache cleared successfully')
        else:
            _print_err('Clearing cache failed')
        return

    if not args['query']:
        parser.print_help()
        return

    if os.getenv('HOWDOI_COLORIZE'):
        args['color'] = True

    if not args['search_engine'] in SUPPORTED_SEARCH_ENGINES:
        _print_err('Unsupported engine.\nThe supported engines are: %s' % ', '.join(SUPPORTED_SEARCH_ENGINES))
        return
    elif args['search_engine'] != 'google':
        os.environ['HOWDOI_SEARCH_ENGINE'] = args['search_engine']

    utf8_result = howdoi(args).encode('utf-8', 'ignore')
    if sys.version < '3':
        print(utf8_result)
    else:
        # Write UTF-8 to stdout: https://stackoverflow.com/a/3603160
        sys.stdout.buffer.write(utf8_result)
    # close the session to release connection
    howdoi_session.close()


if __name__ == '__main__':
    command_line_runner()
