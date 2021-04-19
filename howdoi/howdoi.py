#!/usr/bin/env python

######################################################
#
# howdoi - instant coding answers via the command line
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
######################################################

import gc
gc.disable()

import argparse
import inspect
import json
import os
import re
import sys
import textwrap

from urllib.request import getproxies
from urllib.parse import quote as url_quote, urlparse, parse_qs

from multiprocessing import Pool

import logging
import appdirs
import requests

from cachelib import FileSystemCache, NullCache

from keep import utils as keep_utils

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters.terminal import TerminalFormatter
from pygments.util import ClassNotFound

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import SSLError

from howdoi import __version__
from howdoi.errors import GoogleValidationError, BingValidationError, DDGValidationError

logging.basicConfig(format='%(levelname)s: %(message)s')
if os.getenv('HOWDOI_DISABLE_SSL'):  # Set http instead of https
    SCHEME = 'http://'
    VERIFY_SSL_CERTIFICATE = False
else:
    SCHEME = 'https://'
    VERIFY_SSL_CERTIFICATE = True

SUPPORTED_SEARCH_ENGINES = ('google', 'bing', 'duckduckgo')

URL = os.getenv('HOWDOI_URL') or 'stackoverflow.com'

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
                'Chrome/19.0.1084.46 Safari/536.5'),
               ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
                'Safari/536.5'),)
SEARCH_URLS = {
    'bing': SCHEME + 'www.bing.com/search?q=site:{0}%20{1}&hl=en',
    'google': SCHEME + 'www.google.com/search?q=site:{0}%20{1}&hl=en',
    'duckduckgo': SCHEME + 'duckduckgo.com/html?q=site:{0}%20{1}&t=hj&ia=web'
}

BLOCK_INDICATORS = (
    'form id="captcha-form"',
    'This page appears when Google automatically detects requests coming from your computer '
    'network which appear to be in violation of the <a href="//www.google.com/policies/terms/">Terms of Service'
)

BLOCKED_QUESTION_FRAGMENTS = (
    'webcache.googleusercontent.com',
)

STAR_HEADER = '\u2605'
ANSWER_HEADER = '{2}  Answer from {0} {2}\n{1}'
NO_ANSWER_MSG = '< no answer given >'

CACHE_EMPTY_VAL = "NULL"
CACHE_DIR = appdirs.user_cache_dir('howdoi')
CACHE_ENTRY_MAX = 128

HTML_CACHE_PATH = 'page_cache'
SUPPORTED_HELP_QUERIES = ['use howdoi', 'howdoi', 'run howdoi',
                          'do howdoi', 'howdoi howdoi', 'howdoi use howdoi']

# variables for text formatting, prepend to string to begin text formatting.
BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
UNDERLINE = '\033[4m'
END_FORMAT = '\033[0m'  # append to string to end text formatting.

# stash options
STASH_SAVE = 'save'
STASH_VIEW = 'view'
STASH_REMOVE = 'remove'
STASH_EMPTY = 'empty'

if os.getenv('HOWDOI_DISABLE_CACHE'):
    # works like an always empty cache
    cache = NullCache()
else:
    cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)

howdoi_session = requests.session()


class BlockError(RuntimeError):
    pass


class IntRange:
    def __init__(self, imin=None, imax=None):
        self.imin = imin
        self.imax = imax

    def __call__(self, arg):
        try:
            value = int(arg)
        except ValueError as value_error:
            raise self.exception() from value_error
        if (self.imin is not None and value < self.imin) or (self.imax is not None and value > self.imax):
            raise self.exception()
        return value

    def exception(self):
        if self.imin is not None and self.imax is not None:
            return argparse.ArgumentTypeError(f'Must be an integer in the range [{self.imin}, {self.imax}]')
        if self.imin is not None:
            return argparse.ArgumentTypeError(f'Must be an integer >= {self.imin}')
        if self.imax is not None:
            return argparse.ArgumentTypeError(f'Must be an integer <= {self.imax}')
        return argparse.ArgumentTypeError('Must be an integer')


def _random_int(width):
    bres = os.urandom(width)
    if sys.version < '3':
        ires = int(bres.encode('hex'), 16)
    else:
        ires = int.from_bytes(bres, 'little')

    return ires


def _random_choice(seq):
    return seq[_random_int(1) % len(seq)]


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


def _format_url_to_filename(url, file_ext='html'):
    filename = ''.join(ch for ch in url if ch.isalnum())
    return filename + '.' + file_ext


def _get_result(url):
    try:
        resp = howdoi_session.get(url, headers={'User-Agent': _random_choice(USER_AGENTS)},
                                  proxies=get_proxies(),
                                  verify=VERIFY_SSL_CERTIFICATE)
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.SSLError as error:
        logging.error('%sEncountered an SSL Error. Try using HTTP instead of '
                      'HTTPS by setting the environment variable "HOWDOI_DISABLE_SSL".\n%s', RED, END_FORMAT)
        raise error


def _add_links_to_text(element):
    hyperlinks = element.find('a')

    for hyperlink in hyperlinks:
        pquery_object = pq(hyperlink)
        href = hyperlink.attrib['href']
        copy = pquery_object.text()
        if copy == href:
            replacement = copy
        else:
            replacement = f'[{copy}]({href})'
        pquery_object.replace_with(replacement)


def get_text(element):
    ''' return inner text in pyquery element '''
    _add_links_to_text(element)
    try:
        return element.text(squash_space=False)
    except TypeError:
        return element.text()


def _extract_links_from_bing(html):
    html.remove_namespaces()
    return [a.attrib['href'] for a in html('.b_algo')('h2')('a')]


def _clean_google_link(link):
    if '/url?' in link:
        parsed_link = urlparse(link)
        query_params = parse_qs(parsed_link.query)
        url_params = query_params.get('q', []) or query_params.get('url', [])
        if url_params:
            return url_params[0]
    return link


def _extract_links_from_google(query_object):
    html = query_object.html()
    link_pattern = re.compile(r"https?://*stackoverflow.com/questions/[0-9]*/[a-z0-9-]*")
    links = link_pattern.findall(html)
    links = [_clean_google_link(link) for link in links]
    return links


def _extract_links_from_duckduckgo(html):
    html.remove_namespaces()
    links_anchors = html.find('a.result__a')
    results = []
    for anchor in links_anchors:
        link = anchor.attrib['href']
        url_obj = urlparse(link)
        parsed_url = parse_qs(url_obj.query).get('uddg', '')
        if parsed_url:
            results.append(parsed_url[0])
    return results


def _extract_links(html, search_engine):
    if search_engine == 'bing':
        return _extract_links_from_bing(html)
    if search_engine == 'duckduckgo':
        return _extract_links_from_duckduckgo(html)
    return _extract_links_from_google(html)


def _get_search_url(search_engine):
    return SEARCH_URLS.get(search_engine, SEARCH_URLS['google'])


def _is_blocked(page):
    for indicator in BLOCK_INDICATORS:
        if page.find(indicator) != -1:
            return True

    return False


def _get_links(query):
    search_engine = os.getenv('HOWDOI_SEARCH_ENGINE', 'google')
    search_url = _get_search_url(search_engine).format(URL, url_quote(query))

    logging.info('Searching %s with URL: %s', search_engine, search_url)

    try:
        result = _get_result(search_url)
    except requests.HTTPError:
        result = None
    if not result or _is_blocked(result):
        logging.error('%sUnable to find an answer because the search engine temporarily blocked the request. '
                      'Please wait a few minutes or select a different search engine.%s', RED, END_FORMAT)
        raise BlockError('Temporary block by search engine')

    html = pq(result)
    links = _extract_links(html, search_engine)
    if len(links) == 0:
        logging.info('Search engine %s found no StackOverflow links, returned HTML is:', search_engine)
        logging.info(result)
    return list(dict.fromkeys(links))  # remove any duplicates


def get_link_at_pos(links, position):
    if not links:
        return False

    if len(links) >= position:
        link = links[position - 1]
    else:
        link = links[-1]
    return link


def _format_output(args, code):
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
    for fragment in BLOCKED_QUESTION_FRAGMENTS:
        if fragment in link:
            return False
    return re.search(r'questions/\d+/', link)


def _get_questions(links):
    return [link for link in links if _is_question(link)]


def _get_answer(args, link):  # pylint: disable=too-many-branches
    cache_key = _get_cache_key(link)
    page = cache.get(link)  # pylint: disable=assignment-from-none
    if not page:
        logging.info('Fetching page: %s', link)
        page = _get_result(link + '?answertab=votes')
        cache.set(cache_key, page)
    else:
        logging.info('Using cached page: %s', link)

    html = pq(page)

    first_answer = html('.answercell').eq(0) or html('.answer').eq(0)

    instructions = first_answer.find('pre') or first_answer.find('code')
    args['tags'] = [t.text for t in html('.post-tag')]

    # make decision on answer body class.
    if first_answer.find(".js-post-body"):
        answer_body_cls = ".js-post-body"
    else:
        # rollback to post-text class
        answer_body_cls = ".post-text"

    if not instructions and not args['all']:
        logging.info('No code sample found, returning entire answer')
        text = get_text(first_answer.find(answer_body_cls).eq(0))
    elif args['all']:
        logging.info('Returning entire answer')
        texts = []
        for html_tag in first_answer.items(f'{answer_body_cls} > *'):
            current_text = get_text(html_tag)
            if current_text:
                if html_tag[0].tag in ['pre', 'code']:
                    texts.append(_format_output(args, current_text))
                else:
                    texts.append(current_text)
        text = '\n'.join(texts)
    else:
        text = _format_output(args, get_text(instructions.eq(0)))
    if text is None:
        logging.info('%sAnswer was empty%s', RED, END_FORMAT)
        text = NO_ANSWER_MSG
    text = text.strip()
    return text


def _get_links_with_cache(query):
    cache_key = _get_cache_key(query)
    res = cache.get(cache_key)  # pylint: disable=assignment-from-none
    if res:
        logging.info('Using cached links')
        if res == CACHE_EMPTY_VAL:
            logging.info('No StackOverflow links found in cached search engine results - will make live query')
        else:
            return res

    links = _get_links(query)
    if not links:
        cache.set(cache_key, CACHE_EMPTY_VAL)

    question_links = _get_questions(links)
    cache.set(cache_key, question_links or CACHE_EMPTY_VAL)

    return question_links


def build_splitter(splitter_character='=', splitter_length=80):
    return '\n' + splitter_character * splitter_length + '\n\n'


def _get_answers(args):
    """
    @args: command-line arguments
    returns: array of answers and their respective metadata
             False if unable to get answers
    """

    question_links = _get_links_with_cache(args['query'])
    if not question_links:
        return False

    initial_pos = args['pos'] - 1
    final_pos = initial_pos + args['num_answers']
    question_links = question_links[initial_pos:final_pos]
    search_engine = os.getenv('HOWDOI_SEARCH_ENGINE', 'google')

    logging.info('%s links found on %s: %s', URL, search_engine, len(question_links))
    logging.info('Answers requested: %s, Starting at position: %s', args["num_answers"], args['pos'])

    with Pool() as pool:
        answers = pool.starmap(
            _get_answer_worker,
            [(args, link) for link in question_links]
        )

    for idx, _ in enumerate(answers):
        answers[idx]['position'] = idx + 1

    logging.info('Total answers returned: %s', len(answers))
    return answers


def _get_answer_worker(args, link):
    answer = _get_answer(args, link)
    result = {
        'answer': None,
        'link': None,
        'position': None
    }

    multiple_answers = (args['num_answers'] > 1 or args['all'])

    if not answer:
        return result
    if not args['link'] and not args['json_output'] and multiple_answers:
        answer = ANSWER_HEADER.format(link, answer, STAR_HEADER)
    answer += '\n'

    result['answer'] = answer
    result['link'] = link

    return result


def _clear_cache():
    global cache  # pylint: disable=global-statement,invalid-name
    if not cache:
        cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, 0)

    return cache.clear()


def _is_help_query(query):
    return any(query.lower() == help_query for help_query in SUPPORTED_HELP_QUERIES)


def _format_answers(args, res):
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
    frame = inspect.currentframe()
    calling_func = inspect.getouterframes(frame)[1].function
    return calling_func + str(args) + __version__


def format_stash_item(fields, index=-1):
    title = fields['alias']
    description = fields['desc']
    item_num = index + 1
    if index == -1:
        return f'{UNDERLINE}{BOLD}$ {title}{END_FORMAT}\n\n{description}\n'
    return f'{UNDERLINE}{BOLD}$ [{item_num}] {title}{END_FORMAT}\n\n{description}\n'


def print_stash(stash_list=None):
    if not stash_list or len(stash_list) == 0:
        stash_list = ['\nSTASH LIST:']
        commands = keep_utils.read_commands()
        if commands is None or len(commands.items()) == 0:
            logging.error('%sNo commands found in stash. '
                          'Add a command with "howdoi --%s <query>".%s', RED, STASH_SAVE, END_FORMAT)
            return
        for _, fields in commands.items():
            stash_list.append(format_stash_item(fields))
    else:
        stash_list = [format_stash_item(x['fields'], i) for i, x in enumerate(stash_list)]
    print(build_splitter('#').join(stash_list))


def _get_stash_key(args):
    stash_args = {}
    ignore_keys = [STASH_SAVE, STASH_VIEW, STASH_REMOVE, STASH_EMPTY, 'tags']  # ignore these for stash key
    for key in args:
        if key not in ignore_keys:
            stash_args[key] = args[key]
    return str(stash_args)


def _stash_remove(cmd_key, title):
    commands = keep_utils.read_commands()
    if commands is not None and cmd_key in commands:
        keep_utils.remove_command(cmd_key)
        print(f'\n{BOLD}{GREEN}"{title}" removed from stash{END_FORMAT}\n')
    else:
        print(f'\n{BOLD}{RED}"{title}" not found in stash{END_FORMAT}\n')


def _stash_save(cmd_key, title, answer):
    try:
        keep_utils.save_command(cmd_key, answer, title)
    except FileNotFoundError:
        os.system('keep init')
        keep_utils.save_command(cmd_key, answer, title)
    finally:
        print_stash()


def _parse_cmd(args, res):
    answer = _format_answers(args, res)
    cmd_key = _get_stash_key(args)
    title = ''.join(args['query'])
    if args[STASH_SAVE]:
        _stash_save(cmd_key, title, answer)
        return ''

    if args[STASH_REMOVE]:
        _stash_remove(cmd_key, title)
        return ''
    return answer


def howdoi(raw_query):
    if isinstance(raw_query, str):  # you can pass either a raw or a parsed query
        parser = get_parser()
        args = vars(parser.parse_args(raw_query.split(' ')))
    else:
        args = raw_query

    os.environ['HOWDOI_SEARCH_ENGINE'] = args['search_engine']

    args['query'] = ' '.join(args['query']).replace('?', '')
    cache_key = _get_cache_key(args)

    if _is_help_query(args['query']):
        return _get_help_instructions() + '\n'

    res = cache.get(cache_key)  # pylint: disable=assignment-from-none

    if res:
        logging.info('Using cached response (add -C to clear the cache)')
        return _parse_cmd(args, res)

    logging.info('Fetching answers for query: %s', args["query"])

    try:
        res = _get_answers(args)
        if not res:
            message = 'Sorry, couldn\'t find any help with that topic'
            if not args['explain']:
                message = f'{message} (use --explain to learn why)'
            res = {'error': message}
        cache.set(cache_key, res)
    except (RequestsConnectionError, SSLError):
        res = {'error': f'Unable to reach {args["search_engine"]}. Do you need to use a proxy?\n'}

    return _parse_cmd(args, res)


def get_parser():
    parser = argparse.ArgumentParser(description='instant coding answers via the command line',
                                     epilog=textwrap.dedent('''\
                                     environment variable examples:
                                       HOWDOI_COLORIZE=1
                                       HOWDOI_DISABLE_CACHE=1
                                       HOWDOI_DISABLE_SSL=1
                                       HOWDOI_SEARCH_ENGINE=google
                                       HOWDOI_URL=serverfault.com
                                     '''),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*', help='the question to answer')
    parser.add_argument('-p', '--pos', help='select answer in specified position (default: 1)',
                        default=1, type=IntRange(1, 20), metavar='POS')
    parser.add_argument('-n', '--num', help='number of answers to return (default: 1)',
                        dest='num_answers', default=1, type=IntRange(1, 20), metavar='NUM')
    parser.add_argument('--num-answers', help=argparse.SUPPRESS)
    parser.add_argument('-a', '--all', help='display the full text of the answer', action='store_true')
    parser.add_argument('-l', '--link', help='display only the answer link', action='store_true')
    parser.add_argument('-c', '--color', help='enable colorized output', action='store_true')
    parser.add_argument('-x', '--explain', help='explain how answer was chosen', action='store_true')
    parser.add_argument('-C', '--clear-cache', help='clear the cache',
                        action='store_true')
    parser.add_argument('-j', '--json', help='return answers in raw json format', dest='json_output',
                        action='store_true')
    parser.add_argument('--json-output', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('-v', '--version', help='displays the current version of howdoi',
                        action='store_true')
    parser.add_argument('-e', '--engine', help='search engine for this query (google, bing, duckduckgo)',
                        dest='search_engine', nargs="?", default='google', metavar='ENGINE')
    parser.add_argument('--save', '--stash', help='stash a howdoi answer',
                        action='store_true')
    parser.add_argument('--view', help='view your stash',
                        action='store_true')
    parser.add_argument('--remove', help='remove an entry in your stash',
                        action='store_true')
    parser.add_argument('--empty', help='empty your stash',
                        action='store_true')
    parser.add_argument('--sanity-check', help=argparse.SUPPRESS,
                        action='store_true')
    return parser


def _sanity_check(engine, test_query=None):
    parser = get_parser()
    if not test_query:
        test_query = 'format date bash'

    args = vars(parser.parse_args(test_query.split()))
    args['search_engine'] = engine

    try:
        result = howdoi(args)
        # Perhaps better to use `-j` and then check for an error message
        # rather than trying to enumerate all the error strings
        assert "Sorry" not in result and "Unable to" not in result
    except AssertionError as exc:
        if engine == 'google':
            raise GoogleValidationError from exc
        if engine == 'bing':
            raise BingValidationError from exc
        raise DDGValidationError from exc


def prompt_stash_remove(args, stash_list, view_stash=True):
    if view_stash:
        print_stash(stash_list)

    last_index = len(stash_list)
    prompt = f'{BOLD}> Select a stash command to remove [1-{last_index}] (0 to cancel): {END_FORMAT}'
    user_input = input(prompt)

    try:
        user_input = int(user_input)
        if user_input == 0:
            return
        if user_input < 1 or user_input > last_index:
            logging.error('\n%sInput index is invalid.%s', RED, END_FORMAT)
            prompt_stash_remove(args, stash_list, False)
            return
        cmd = stash_list[user_input - 1]
        cmd_key = cmd['command']
        cmd_name = cmd['fields']['alias']
        _stash_remove(cmd_key, cmd_name)
        return
    except ValueError:
        logging.error('\n%sInvalid input. Must specify index of command.%s', RED, END_FORMAT)
        prompt_stash_remove(args, stash_list, False)
        return


def perform_sanity_check():
    '''Perform sanity check.
    Returns exit code for program. An exit code of -1 means a validation error was encountered.
    '''
    global cache  # pylint: disable=global-statement,invalid-name
    # Disable cache to avoid cached answers while performing the checks
    cache = NullCache()

    exit_code = 0
    for engine in ('google', 'bing', 'duckduckgo'):
        print('Checking {}...'.format(engine))
        try:
            _sanity_check(engine)
        except (GoogleValidationError, BingValidationError, DDGValidationError):
            logging.error('%s%s query failed%s', RED, engine, END_FORMAT)
            exit_code = -1
    if exit_code == 0:
        print(f'{GREEN}Ok{END_FORMAT}')
    return exit_code


def command_line_runner():  # pylint: disable=too-many-return-statements,too-many-branches
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if args['explain']:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('Version: %s', __version__)

    if args['sanity_check']:
        sys.exit(
            perform_sanity_check()
        )

    if args['clear_cache']:
        if _clear_cache():
            print(f'{GREEN}Cache cleared successfully{END_FORMAT}')
        else:
            logging.error('%sClearing cache failed%s', RED, END_FORMAT)

    if args[STASH_VIEW]:
        print_stash()
        return

    if args[STASH_EMPTY]:
        os.system('keep init')
        return

    if args[STASH_REMOVE] and len(args['query']) == 0:
        commands = keep_utils.read_commands()
        if commands is None or len(commands.items()) == 0:
            logging.error('%sNo commands found in stash. '
                          'Add a command with "howdoi --%s <query>".%s', RED, STASH_SAVE, END_FORMAT)
            return
        stash_list = [{'command': cmd, 'fields': field} for cmd, field in commands.items()]
        prompt_stash_remove(args, stash_list)
        return

    if not args['query']:
        parser.print_help()
        return

    if os.getenv('HOWDOI_COLORIZE'):
        args['color'] = True

    if not args['search_engine'] in SUPPORTED_SEARCH_ENGINES:
        logging.error('Unsupported engine.\nThe supported engines are: %s' ', '.join(SUPPORTED_SEARCH_ENGINES))
        return

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
