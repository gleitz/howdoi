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
import webbrowser

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
    return (url, [a.attrib['href'] for a in html('.l')])

def get_duck_links(query):
    url = DUCK_SEARCH_URL.format(urllib.quote(query))
    result = get_result(url)
    html = pq(result)
    links = [l.find('a').attrib['href'] for l in html('.links_main')]

def get_link_at_pos(links, pos):
    pos = int(pos) - 1
    questions = [link for link in links if is_question(link)]
    if pos < len(questions):
        return questions[pos]

def get_instructions(args):
    search_url, links = get_google_links(args['query'])
    if not links:
        return search_url, None

    link = get_link_at_pos(links, args['pos'])
    if args.get('link'):
        return search_url, link

    link = link + '?answertab=votes'
    page = get_result(link)
    html = pq(page)
    first_answer = html('.answer').eq(0)
    instructions = first_answer.find('pre') or first_answer.find('code')
    if args['all'] or not instructions:
        text = first_answer.find('.post-text').eq(0).text()
    else:
        text = instructions.eq(0).text()
    return search_url, text

def howdoi(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    search_url, instructions = get_instructions(args)
    if not instructions:
        print 'Sorry, couldn\'t find any help with that topic'
        return
    print instructions
    if args['interactive']:
        result = raw_input("Find what you needed? Type no to open the search url\n")
        if "no" == result:
            print search_url
            webbrowser.open(search_url, new=2, autoraise=True)

def command_line_runner():
    parser = argparse.ArgumentParser(description='code search tool')
    parser.add_argument('query', metavar='QUERY', type=str, nargs=argparse.REMAINDER,
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='select answer in specified position (default: 1)', default=1)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('-i','--interactive', help='Print results and search link in interactive mode',
                        action='store_true')
    args = vars(parser.parse_args())
    howdoi(args)

if __name__ == '__main__':
    command_line_runner()
