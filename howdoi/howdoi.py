#!/usr/bin/env python

######################################################
#
# howdoi - instant coding answers via the command line
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
######################################################

import argparse
import random
import re
import requests
import sys

try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

try:
    from urllib import getproxies as get_proxies
except ImportError:
    from urllib import request
    get_proxies = request.getproxies

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

SEARCH_URL = 'https://www.google.com/search?q=site:stackoverflow.com%20{0}'
USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)
ANSWER_HEADER = u('--- Answer {0} ---\n{1}')
NO_ANSWER_MSG = '< no answer given >'

def get_result(url):
    return requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_proxies()).text


def is_question(link):
    return re.search('questions/\d+/', link)


def get_links(query):
    url = SEARCH_URL.format(url_quote(query))
    result = get_result(url)
    html = pq(result)
    return [a.attrib['href'] for a in html('.l')] or \
        [a.attrib['href'] for a in html('.r')('a')]


def get_link_at_pos(links, pos):
    for link in links:
        if is_question(link):
            if pos == 1:
                break
            else:
                pos = pos - 1
                continue
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

    return highlight(
        code,
        lexer,
        TerminalFormatter(bg='dark')
    )


def get_answer(args, links):
    link = get_link_at_pos(links, args['pos'])
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
    links = get_links(args['query'])
    if not links:
        return ''
    answers = []
    append_header = args['num_answers'] > 1
    initial_position = args['pos']
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


def howdoi(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    try:
        return get_instructions(args) or 'Sorry, couldn\'t find any help with that topic\n'
    except ConnectionError:
        return 'Failed to establish network connection\n'


def get_parser():
    parser = argparse.ArgumentParser(description='instant coding answers via the command line')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='+',
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='select answer in specified position (default: 1)', default=1, type=int)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-c', '--color', help='enable colorized output',
                        action='store_true')
    parser.add_argument('-n','--num-answers', help='number of answers to return', default=1, type=int)
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    print(howdoi(args).encode("utf-8", "ignore"))

if __name__ == '__main__':
    command_line_runner()
