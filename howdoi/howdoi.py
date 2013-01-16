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
import urllib

from pyquery import PyQuery as pq

GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site:stackoverflow.com%20{0}"
DUCK_SEARCH_URL = "http://duckduckgo.com/html?q=site%3Astackoverflow.com%20{0}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"


def get_result(url):
    return requests.get(url, headers={'User-Agent': USER_AGENT}).text


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
    pos = pos - 1
    for link in links:
        if is_question(link):
            if pos == 0:
                break
            else:
                pos = pos - 1
                continue
    return link


def get_instructions(query, position, link_only, all_text):
    links = get_google_links(query)
    if not links:
        return ''

    link = get_link_at_pos(links, position)
    if link_only:
        return link

    link = link + '?answertab=votes'
    page = get_result(link)
    html = pq(page)
    first_answer = html('.answer').eq(0)
    instructions = first_answer.find('pre') or first_answer.find('code')
    if all_text or not instructions:
        text = first_answer.find('.post-text').eq(0).text()
    else:
        text = instructions.eq(0).text()
    if not text:
        return ''
    return text

def get_multiple_instructions(args):
    initial_position = args['pos']
    assert args['number_of_results'] > 1
    
    for result_number in range(args['number_of_results']):
      current_position = result_number + initial_position
      instructions = get_instructions(args['query'], current_position, args['link'], args['all'])
      if instructions:
        print """
----------------------
Result %s

%s
""" % (current_position, instructions)

def howdoi(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
  
    if args['number_of_results'] > 1:
      return get_multiple_instructions(args)
    
    instructions = get_instructions(args['query'], args['pos'], args['link'], args['all']) or 'Sorry, couldn\'t find any help with that topic'
    print instructions


def command_line_runner():
    parser = argparse.ArgumentParser(description='code search tool')
    parser.add_argument('query', metavar='QUERY', type=str, nargs=argparse.REMAINDER,
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='select answer in specified position (default: 1)', default=1, type=int)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-n','--number-of-results', help='number of results to return', default=1, type=int)
    args = vars(parser.parse_args())
    howdoi(args)

if __name__ == '__main__':
    command_line_runner()
