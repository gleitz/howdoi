#!/usr/bin/env python

######################################################
#
# howdoi - instant coding answers via the command line
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
######################################################

import argparse
import glob
import os
import random
import re
import requests
import requests_cache
import sys
from . import __version__

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters.terminal import TerminalFormatter
from pygments.util import ClassNotFound

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError

# Handle imports for Python 2 and 3
if sys.version < '3':
    import codecs
    from urllib import quote as url_quote
    from urllib import getproxies

    # Handling Unicode: http://stackoverflow.com/a/6633040/305414
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    from urllib.request import getproxies
    from urllib.parse import quote as url_quote

    def u(x):
        return x


if os.getenv('HOWDOI_DISABLE_SSL'):  # Set http instead of https
    SEARCH_URL = 'http://www.google.com/search?q=site:{0}%20{1}'
    VERIFY_SSL_CERTIFICATE = False
else:
    SEARCH_URL = 'https://www.google.com/search?q=site:{0}%20{1}'
    VERIFY_SSL_CERTIFICATE = True

URL = os.getenv('HOWDOI_URL') or 'stackoverflow.com'

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
                'Chrome/19.0.1084.46 Safari/536.5'),
               ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
                'Safari/536.5'), )
STAR_HEADER = u('\u2605')
ANSWER_HEADER = u('{2}  Answer from {0} {2}\n{1}')
NO_ANSWER_MSG = '< no answer given >'
XDG_CACHE_DIR = os.environ.get('XDG_CACHE_HOME',
                               os.path.join(os.path.expanduser('~'), '.cache'))
CACHE_DIR = os.path.join(XDG_CACHE_DIR, 'howdoi')
CACHE_FILE = os.path.join(CACHE_DIR, 'cache{0}'.format(
    sys.version_info[0] if sys.version_info[0] == 3 else ''))


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


def _get_result(url):
    try:
        return requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_proxies(),
                            verify=VERIFY_SSL_CERTIFICATE).text
    except requests.exceptions.SSLError as e:
        print('[ERROR] Encountered an SSL Error. Try using HTTP instead of '
              'HTTPS by setting the environment variable "HOWDOI_DISABLE_SSL".\n')
        raise e


def _get_links(query):
    result = _get_result(SEARCH_URL.format(URL, url_quote(query)))
    html = pq(result)
    return [a.attrib['href'] for a in html('.l')] or \
        [a.attrib['href'] for a in html('.r')('a')]


def get_link_at_pos(links, position):
    if not links:
        return False

    if len(links) >= position:
        link = links[position - 1]
    else:
        link = links[-1]
    return link


def _format_output(code, args):
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
        try:
            lexer = guess_lexer(code)
        except ClassNotFound:
            return code

    return highlight(code,
                     lexer,
                     TerminalFormatter(bg='dark'))


def _is_question(link):
    return re.search('questions/\d+/', link)


def _get_questions(links):
    return [link for link in links if _is_question(link)]


def _get_answer(args, links):
    link = get_link_at_pos(links, args['pos'])
    if not link:
        return False
    if args.get('link'):
        return link
    page = _get_result(link + '?answertab=votes')
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
                    texts.append(_format_output(current_text, args))
                else:
                    texts.append(current_text)
        text = '\n'.join(texts)
    else:
        text = _format_output(instructions.eq(0).text(), args)
    if text is None:
        text = NO_ANSWER_MSG
    text = text.strip()
    return text


def _get_instructions(args):
    links = _get_links(args['query'])
    question_links = _get_questions(links)

    only_hyperlinks = args.get('link')
    star_headers = (args['num_answers'] > 1 or args['all'])

    if not links:
        return False
    answers = []
    initial_position = args['pos']
    for answer_number in range(args['num_answers']):
        current_position = answer_number + initial_position
        args['pos'] = current_position
        link = get_link_at_pos(question_links, current_position)
        answer = _get_answer(args, question_links)
        if not answer:
            continue
        if not only_hyperlinks:
            answer = format_answer(link, answer, star_headers)
        answer += '\n'
        answers.append(answer)
    return '\n'.join(answers)

def format_answer(link, answer, star_headers):
    if star_headers:
        return ANSWER_HEADER.format(link, answer, STAR_HEADER)
    else:
        return answer

def _enable_cache():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    requests_cache.install_cache(CACHE_FILE)


def _clear_cache():
    for cache in glob.glob('{0}*'.format(CACHE_FILE)):
        os.remove(cache)


def howdoi(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    try:
        return _get_instructions(args) or 'Sorry, couldn\'t find any help with that topic\n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'


def get_parser():
    parser = argparse.ArgumentParser(description='instant coding answers via the command line')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*',
                        help='the question to answer')
    parser.add_argument('-p', '--pos', help='select answer in specified position (default: 1)', default=1, type=int)
    parser.add_argument('-a', '--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l', '--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-c', '--color', help='enable colorized output',
                        action='store_true')
    parser.add_argument('-n', '--num-answers', help='number of answers to return', default=1, type=int)
    parser.add_argument('-C', '--clear-cache', help='clear the cache',
                        action='store_true')
    parser.add_argument('-v', '--version', help='displays the current version of howdoi',
                        action='store_true')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if args['clear_cache']:
        _clear_cache()
        print('Cache cleared successfully')
        return

    if not args['query']:
        parser.print_help()
        return

    # enable the cache if user doesn't want it to be disabled
    if not os.getenv('HOWDOI_DISABLE_CACHE'):
        _enable_cache()

    if os.getenv('HOWDOI_COLORIZE'):
        args['color'] = True

    utf8_result = howdoi(args).encode('utf-8', 'ignore')
    if sys.version < '3':
        print(utf8_result)
    else:
        # Write UTF-8 to stdout: https://stackoverflow.com/a/3603160
        sys.stdout.buffer.write(utf8_result)


if __name__ == '__main__':
    command_line_runner()
