#!/usr/bin/env python

######################################################
#
# howdou - instant coding answers via the command line
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
######################################################

import argparse
import datetime
import glob
import os
import random
import re
import requests
import requests_cache
import sys
import time

try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

try:
    from urllib import getproxies
except ImportError:
    from urllib.request import getproxies

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError

import yaml
from elasticsearch import Elasticsearch
import dateutil.parser

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

KNOWLEDGEBASE_FN = os.path.expanduser(os.getenv('HOWDOU_KB', '~/.howdou.yml'))
KNOWLEDGEBASE_INDEX = os.getenv('HOWDOU_INDEX', 'howdou')
KNOWLEDGEBASE_TIMESTAMP_FN = os.path.expanduser(os.getenv('HOWDOU_TIMESTAMP', '~/.howdou_last'))

if os.getenv('HOWDOU_DISABLE_SSL'):  # Set http instead of https
    SEARCH_URL = 'http://www.google.com/search?q=site:{0}%20{1}'
else:
    SEARCH_URL = 'https://www.google.com/search?q=site:{0}%20{1}'

LOCALIZATION = os.getenv('HOWDOU_LOCALIZATION') or 'en'

LOCALIZATON_URLS = {
    'en': 'stackoverflow.com',
    'pt-br': 'pt.stackoverflow.com',
}

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)
ANSWER_HEADER = u('--- Answer {0} ---\n{1}')
NO_ANSWER_MSG = '< no answer given >'
XDG_CACHE_DIR = os.environ.get('XDG_CACHE_HOME',
                               os.path.join(os.path.expanduser('~'), '.cache'))
CACHE_DIR = os.path.join(XDG_CACHE_DIR, 'howdou')
CACHE_FILE = os.path.join(CACHE_DIR, 'cache{0}'.format(
        sys.version_info[0] if sys.version_info[0] == 3 else ''))

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)

def is_kb_updated():
    if not os.path.isfile(KNOWLEDGEBASE_TIMESTAMP_FN):
        return True
    kb_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(KNOWLEDGEBASE_FN))
    timestamp_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(KNOWLEDGEBASE_TIMESTAMP_FN))
    modified = kb_last_modified > timestamp_last_modified
    return modified

def update_kb_timestamp():
    touch(KNOWLEDGEBASE_TIMESTAMP_FN)

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


def get_result(url):
    try:
        return requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_proxies()).text
    except requests.exceptions.SSLError as e:
        print('[ERROR] Encountered an SSL Error. Try using HTTP instead of '
              'HTTPS by setting the environment variable "HOWDOU_DISABLE_SSL".\n')
        raise e


def is_question(link):
    return re.search('questions/\d+/', link)


def get_links(query):
    localization_url = LOCALIZATON_URLS[LOCALIZATION]
    result = get_result(SEARCH_URL.format(localization_url, url_quote(query)))
    html = pq(result)
    return [a.attrib['href'] for a in html('.l')] or \
        [a.attrib['href'] for a in html('.r')('a')]


def get_link_at_pos(links, position):
    links = [link for link in links if is_question(link)]
    if not links:
        return False

    if len(links) >= position:
        link = links[position-1]
    else:
        link = links[-1]
    return link


def format_output(code, args):
    if not args['color']:
        return code
    lexer = None

    # try to find a lexer using the StackOverflow tags
    # or the query arguments
    for keyword in args['query'].split() + args['tags']:
        try:
            lexer = get_lexer_by_name(keyword)
            break
        except ClassNotFound:
            pass

    # no lexer found above, use the guesser
    if not lexer:
        lexer = guess_lexer(code)

    return highlight(code,
                     lexer,
                     TerminalFormatter(bg='dark'))


def get_answer(args, links):
    link = get_link_at_pos(links, args['pos'])
    if not link:
        return False
    if args.get('link'):
        return link
    page = get_result(link + '?answertab=votes')
    html = pq(page)

    first_answer = html('.answer').eq(0)
    instructions = first_answer.find('pre') or first_answer.find('code')
    args['tags'] = [t.text for t in html('.post-tag')]

    if not instructions and not args['all']:
        text = first_answer.find('.post-text').eq(0).text()
    elif args['all']:
        texts = []
        for html_tag in first_answer.items('.post-text > *'):
            current_text = html_tag.text()
            if current_text:
                if html_tag[0].tag in ['pre', 'code']:
                    texts.append(format_output(current_text, args))
                else:
                    texts.append(current_text)
        texts.append('\n---\nAnswer from {0}'.format(link))
        text = '\n'.join(texts)
    else:
        text = format_output(instructions.eq(0).text(), args)
    if text is None:
        text = NO_ANSWER_MSG
    text = text.strip()
    return text


def get_instructions(args):
    answers = []
    append_header = args['num_answers'] > 1
    initial_position = args['pos']
    query = args['query']
    
    # Check local index first.
    #http://elasticsearch.org/guide/reference/query-dsl/
    #http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
    es = Elasticsearch()
    results = es.search(
        index=KNOWLEDGEBASE_INDEX,
        body={
            'query':{
##                'query_string':{ # search all text fields
##                    'query':query,
##                },
#                'field':{
#                    'questions':{
#                        'query':query,
#                    }
#                },
                "function_score": {
                    "query": {  
                        "match": {
                            "questions": query
                        }
                    },
                    "functions": [{
                        "script_score": { 
                            "script": "doc['weight'].value"
                        }
                    }],
                    "score_mode": "multiply"
                }
            },
#            'query':{
#                'field':{
#                    'questions':{
#                        'query':query,
#                    }
#                },
#            },
        },
    )
#    from pprint import pprint
#    pprint(results['hits']['hits'],indent=4)
    hits = results['hits']['hits'][:args['num_answers']]
    if hits:
        answer_number = -1
        for hit in hits:
            answer_number += 1
            current_position = answer_number + initial_position
            answer = hit['_source']['answer'].strip()
            #TODO:sort/boost by weight?
            #TODO:ignore low weights?
            score = hit['_score']
            if score < float(args['min_score']):
                continue
            if args['show_score']:
                answer = ('score: %s\n' % score) + answer
            if append_header:
                answer = ANSWER_HEADER.format(current_position, answer)
            answer = answer + '\n'
            answers.append(answer)
    
    # If we found nothing satisfying locally, then search the net.
    if not answers:
        links = get_links(query)
        if not links:
            return False
        for answer_number in range(args['num_answers']):
            current_position = answer_number + initial_position
            args['pos'] = current_position
            answer = get_answer(args, links)
            if not answer:
                continue
            if append_header:
                answer = ANSWER_HEADER.format(current_position, answer)
            answer = answer + '\n'
            answers.append(answer)
            
    return '\n'.join(answers)


def enable_cache():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    requests_cache.install_cache(CACHE_FILE)


def clear_cache():
    for cache in glob.glob('{0}*'.format(CACHE_FILE)):
        os.remove(cache)


def howdou(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    try:
        return get_instructions(args) or 'Sorry, couldn\'t find any help with that topic\n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'

def init_kb():
    kb_fn = os.path.expanduser(KNOWLEDGEBASE_FN)
    if not os.path.isfile(kb_fn):
        open(kb_fn, 'w').write('''-   questions:
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
''')

def index_kb():
    print 'Re-indexing...'
    es = Elasticsearch()
    count = 0
    for item in yaml.load(open(os.path.expanduser(KNOWLEDGEBASE_FN))):
        #print item
        questions = '\n'.join(item['questions'])
        for answer in item['answers']:
            count += 1
            #print count,answer
            weight = float(answer.get('weight', 1))
            dt = answer['date']
            if isinstance(dt, basestring):
                dt = dateutil.parser.parse(dt)
            es.index(
                index=KNOWLEDGEBASE_INDEX,
                doc_type='text',
                id=count,
#                properties=dict(
#                    text=dict(type='string', boost=weight)
#                ),
                body=dict(
                    questions=questions,
                    answer=answer['text'],
                    text=questions + ' ' + answer['text'],
                    timestamp=dt,
                    weight=weight,
                ),
            )
    es.indices.refresh(index=KNOWLEDGEBASE_INDEX)
    update_kb_timestamp()
    print 'Re-indexed %i items.' % (count,)

def get_parser():
    parser = argparse.ArgumentParser(description='instant coding answers via the command line')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*',
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='select answer in specified position (default: 1)', default=1, type=int)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-c', '--color', help='enable colorized output',
                        action='store_true')
    parser.add_argument('-n','--num-answers', help='number of answers to return', default=1, type=int)
    parser.add_argument('--min-score', help='the minimum score accepted on local answers', default=1, type=float)
    parser.add_argument('-C','--clear-cache', help='clear the cache',
                        action='store_true')
    parser.add_argument('--reindex', help='refresh the elasticsearch index', default=False,
                        action='store_true')
    parser.add_argument('--show-score', help='display score of all results', default=False,
                        action='store_true')
    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['clear_cache']:
        clear_cache()
        print('Cache cleared successfully')
        return

    init_kb()
    if args['reindex'] or is_kb_updated():
        index_kb()

    if not args['query']:
        parser.print_help()
        return

    # enable the cache if user doesn't want it to be disabled
    if not os.getenv('HOWDOU_DISABLE_CACHE'):
        enable_cache()

    print
    if sys.version < '3':
        print(howdou(args).encode('utf-8', 'ignore'))
    else:
        print(howdou(args))



if __name__ == '__main__':
    command_line_runner()
