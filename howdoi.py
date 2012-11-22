#!/usr/bin/python

##################################################
#
# howdoi - a unix code search tool.
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
##################################################

import urllib
import urllib2
import sys
import json

from BeautifulSoup import BeautifulSoup as bs

SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCo6SQ6XNvvS3fdJLcDNR4mpdIGGmVcXAk&cx=015163316206774170098:pj94ujarmcg&q={0}&alt=json"

def get_result(url):
    result = urllib2.urlopen(url)
    return result.read()

def get_instructions(query):
    url = SEARCH_URL.format(urllib.quote(query))
    result = get_result(url)
    if not result:
        return ''
    else:
        response = json.loads(result)
        try:
            link = response['items'][0]['link']
            page = get_result(link)
            soup = bs(page)
            first_answer = soup.find("div", {"id": "answers"})
            instructions = first_answer.find("code") or first_answer.find("pre")
            return instructions.text
        except:
            return ''


def howdoi(query):
    instructions = get_instructions(query) or "Sorry, couldn't find any help with that topic"
    print instructions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: howdoi query (e.g. howdoi format date bash)"
    else:
        howdoi(" ".join(sys.argv[1:]))
