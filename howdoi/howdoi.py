#!/usr/bin/env python

##################################################
#
# howdoi - a code search tool.
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
##################################################

import argparse
import re
import requests

try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError

SEARCH_URL = 'https://www.google.com/search?q=site:stackoverflow.com%20{0}'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'
ANSWER_HEADER = u'--- Answer {0} ---\n{1}'


def get_result(url):
    return requests.get(url, headers={'User-Agent': USER_AGENT}).text


def is_question(link):
    return re.search('questions/\d+/', link)


def get_links(query):
    url = SEARCH_URL.format(url_quote(query))
    result = get_result(url)
    html = pq(result)
    return [a.attrib['href'] for a in html('.l')]


def get_link_at_pos(links, pos):
    pos = pos - 1
    for link in links:
        if is_question(link):
            if pos == 0:
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

    if not instructions:
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
        texts.append('\n---\nAnswer from %s' % link)
        text = "\n".join(texts)
    else:
        text = format_output(instructions.eq(0).text(), args)
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
    return u'\n'.join(answers)


def howdoi(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    try:
        instructions = get_instructions(args) or 'Sorry, couldn\'t find any help with that topic\n'
        print(instructions)
    except ConnectionError:
        print('Failed to establish network connection\n')


def command_line_runner():
    parser = argparse.ArgumentParser(description='code search tool')
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
    args = vars(parser.parse_args())
    howdoi(args)

if __name__ == '__main__':
    command_line_runner()
