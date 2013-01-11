#!/usr/bin/env python

##################################################
#
# howdoi - a code search tool.
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
##################################################

import urllib
import urllib2
import sys
import json
import argparse
import re
import os
import shelve

from pyquery import PyQuery as pq

DESCRIPTION = """Howdoi is a code search tool which will answer
                 all sorts of queries, doing the research for you."""

GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site:stackoverflow.com%20{0}"
DUCK_SEARCH_URL = "http://duckduckgo.com/html?q=site%3Astackoverflow.com%20{0}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"

CACHE_FILE = os.path.join( os.path.expanduser('~'),
                           '.howdoi.cache' )

def get_result(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', USER_AGENT)]
    result = opener.open(url)
    return result.read()

def is_question(link):
    return re.search('questions/\d+/', link)

def get_google_links(query):
    url = GOOGLE_SEARCH_URL.format(urllib.quote(query))
    result = get_result(url)
    html = pq(result)
    return [a.attrib['href'] for a in html('.l')]

def get_duck_links(query):
    url = DUCK_SEARCH_URL.format(urllib.quote(query))
    result = get_result(url)
    html = pq(result)
    links = [l.find('a').attrib['href'] for l in html('.links_main')]

def get_link_at_pos(links, pos):
    pos = int(pos) - 1
    for link in links:
        if is_question(link):
            if pos == 0:
                break
            else:
                pos = pos - 1
                continue
    return link

def get_instructions(args):
    links = get_google_links(args['query'])
    if not links:
        return ''
    link = get_link_at_pos(links, args['pos'])
    if args.get('link'):
        return link
    link = link + '?answertab=votes'
    page = get_result(link)
    html = pq(page)
    first_answer = html('.answer').eq(0)
    instructions = first_answer.find('pre') or first_answer.find('code')

    if args['all'] or not instructions:
        text = first_answer.find('.post-text').eq(0).text()
    else:
        text = instructions.eq(0).text()

    return text or ''

def retrieve_last_query(cache):
    """
    Retrieve the last executed query and answer index
    from the cache file
    """
    return cache.get('last_query', { 'query':'', 'pos':1 })

def store_last_query(cache, query, pos=1):
    """
    Store a query and the index of the answer
    in the cache for later retrieval
    """
    cache['last_query'] = { 'query':query, 'pos':pos }

def howdoi(args, cache):
    query = args['query']
    pos = args['pos']

    if args['again'] or args['next']:
        last_query = retrieve_last_query(cache)
        query = last_query['query']
        pos = last_query['pos']
        if args['next']: pos = pos + 1
        print '> howdoi -p %d %s\n' % (pos, query)
    else:
        query = ' '.join(query).replace('?', '')

    args['query'] = query
    args['pos'] = pos

    print get_instructions(args) or 'Sorry, couldn\'t find any help with that topic'
    store_last_query(cache, args['query'], args['pos'])

def command_line_runner():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('query', metavar='QUERY', type=str, nargs=argparse.REMAINDER,
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='display the n-th found answer (default: 1)',
                        default=1)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-g','--again', help='execute the last query again',
                        action='store_true')
    parser.add_argument('-n','--next', help='display the next answer for the last query',
                        action='store_true')
    args = vars(parser.parse_args())

    if not (args['query'] or args['again'] or args['next']):
        return parser.print_usage()

    cache = shelve.open(CACHE_FILE, writeback=True)
    howdoi(args, cache)
    cache.close()

if __name__ == '__main__':
    command_line_runner()
