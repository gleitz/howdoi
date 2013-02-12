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
    for link in links:
        if is_question(link):
            if pos == 1:
                break
            else:
                pos = pos - 1
                continue
    return link


def get_answer(args, links):
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
        return get_instructions(args) or 'Sorry, couldn\'t find any help with that topic\n'
    except ConnectionError:
        return 'Failed to establish network connection\n'


def get_parser():
    parser = argparse.ArgumentParser(description='code search tool')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='+',
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='select answer in specified position (default: 1)', default=1, type=int)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-n','--num-answers', help='number of answers to return', default=1, type=int)
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    print(howdoi(args))

if __name__ == '__main__':
    command_line_runner()
