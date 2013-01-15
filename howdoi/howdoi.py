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

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"


class Search(object):
    user_agent = USER_AGENT

    def get(self, query):
        url = self.url.format(url_quote(query))
        result = requests.get(url, headers={'User-Agent': self.user_agent})
        html = pq(result.text)
        return html

    def links(self, query):
        raise NotImplemented

    def link(self, query, position=0):
        for pos, link in enumerate(self.links(query)):
            if pos == position:
                return link

    def is_question(self, link):
        return re.search('questions/\d+/', link)


class GoogleSearch(Search):
    url = "https://www.google.com/search?q=site:stackoverflow.com%20{0}"

    def links(self, query):
        html = super(GoogleSearch, self).get(query)
        for a in html('.l'):
            href = a.attrib['href']
            if self.is_question(href):
                yield href


class DuckDuckGoSearch(Search):
    url = "http://duckduckgo.com/html?q=site%3Astackoverflow.com%20{0}"

    def links(self, query):
        html = super(DuckDuckGoSearch, self).get(query)
        for a in html('.links_main'):
            href = a.find('a').attrib['href']
            if self.is_question(href):
                yield href


class StackOverflowInstructions(object):
    user_agent = USER_AGENT

    def get(self, link):
        link += '?answertab=votes'
        result = requests.get(link, headers={'User-Agent': self.user_agent})
        html = pq(result.text)
        return html

    def instructions(self, link, position=0, complete=False):
        html = self.get(link)
        answer = html('.answer').eq(position)
        instructions = answer.find('pre') or answer.find('code')
        if complete or not instructions:
            text = answer.find('.post-text').eq(0).text()
        else:
            text = instructions.eq(0).text()
        return text or ''


def get_instructions(args):
    #search = DuckDuckGoSearch()
    search = GoogleSearch()
    instructions = StackOverflowInstructions()

    query = ' '.join(args['query']).replace('?', '')
    position = int(args['pos']) - 1
    link = search.link(query, position)

    if args.get('link'):
        response = link
    else:
        response = instructions.instructions(link, complete=args['all'])
    return response or 'Sorry, couldn\'t find any help with that topic'


def command_line_runner():
    parser = argparse.ArgumentParser(description='code search tool')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='+',
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='select answer in specified position (default: 1)', default=1)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    args = vars(parser.parse_args())
    print(get_instructions(args))

if __name__ == '__main__':
    command_line_runner()
