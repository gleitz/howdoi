#!/usr/bin/python

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

from pyquery import PyQuery as pq

GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site:stackoverflow.com%20{0}"
DUCK_SEARCH_URL = "http://duckduckgo.com/html?q=site%3Astackoverflow.com%20{0}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"

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
    pos = int(args['pos']) - 1
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
    if args['full'] or not instructions:
        text = first_answer.find('.post-text').eq(0).text()
    else:
        text = instructions.eq(0).text()
    if not text:
        return ''
    return text

def howdoi(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    instructions = get_instructions(args) or 'Sorry, couldn\'t find any help with that topic'
    print instructions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='code search tool')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='+',
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='return answer in specified position (default: 1)', default=1)
    parser.add_argument('-f','--full', help='return the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    args = vars(parser.parse_args())
    howdoi(args)
