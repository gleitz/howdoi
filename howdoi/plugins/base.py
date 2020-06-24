import os
import re
import sys

import appdirs

from cachelib import FileSystemCache, NullCache

from pyquery import PyQuery as pq


class BlockError(RuntimeError):
    pass


# Handle imports for Python 2 and 3
if sys.version < '3':
    import codecs
    from urllib import quote as url_quote
    from urllib import getproxies
    from urlparse import urlparse, parse_qs

    # Handling Unicode: http://stackoverflow.com/a/6633040/305414
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    from urllib.request import getproxies
    from urllib.parse import quote as url_quote, urlparse, parse_qs

    def u(x):
        return x

# rudimentary standardized 3-level log output


def _print_err(x):
    print("[ERROR] " + x)


_print_ok = print  # noqa: E305


def _print_dbg(x):
    print("[DEBUG] " + x)  # noqa: E302


CACHE_EMPTY_VAL = "NULL"
CACHE_DIR = appdirs.user_cache_dir('howdoi')
CACHE_ENTRY_MAX = 128

if os.getenv('HOWDOI_DISABLE_CACHE'):
    cache = NullCache()  # works like an always empty cache
else:
    cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)

ANSWER_HEADER = u('{2}  Answer from {0} {2}\n{1}')
STAR_HEADER = u('\u2605')
CACHE_EMPTY_VAL = "NULL"
NO_ANSWER_MSG = '< no answer given >'

if os.getenv('HOWDOI_DISABLE_SSL'):  # Set http instead of https
    SCHEME = 'http://'
    VERIFY_SSL_CERTIFICATE = False
else:
    SCHEME = 'https://'
    VERIFY_SSL_CERTIFICATE = True

BLOCK_INDICATORS = (
    'form id="captcha-form"',
    'This page appears when Google automatically detects requests coming from your computer '
    'network which appear to be in violation of the <a href="//www.google.com/policies/terms/">Terms of Service'
)

URL = os.getenv('HOWDOI_URL') or 'stackoverflow.com'

SEARCH_URLS = {
    'bing': SCHEME + 'www.bing.com/search?q=site:{0}%20{1}&hl=en',
    'google': SCHEME + 'www.google.com/search?q=site:{0}%20{1}&hl=en',
    'duckduckgo': SCHEME + 'duckduckgo.com/?q=site:{0}%20{1}&t=hj&ia=web'
}


def _is_blocked(page):
    for indicator in BLOCK_INDICATORS:
        if page.find(indicator) != -1:
            return True
    return False


class BasePlugin():
    def search(self):
        print("Hello search")
        pass

    def _add_links_to_text(self, element):
        hyperlinks = element.find('a')

        for hyperlink in hyperlinks:
            pquery_object = pq(hyperlink)
            href = hyperlink.attrib['href']
            copy = pquery_object.text()
            if (copy == href):
                replacement = copy
            else:
                replacement = "[{0}]({1})".format(copy, href)
            pquery_object.replace_with(replacement)

    def get_link_at_pos(self, links, position):
        if not links:
            return False
        if len(links) >= position:
            link = links[position - 1]
        else:
            link = links[-1]
        return link

    def get_text(self, element):
        ''' return inner text in pyquery element '''
        self._add_links_to_text(element)
        try:
            return element.text(squash_space=False)
        except TypeError:
            return element.text()

    def _get_search_url(self, search_engine):
        return SEARCH_URLS.get(search_engine, SEARCH_URLS['google'])

    def _get_links(self, query):
        search_engine = os.getenv('HOWDOI_SEARCH_ENGINE', 'google')
        search_url = self._get_search_url(search_engine)

        result = self._get_result(search_url.format(URL, url_quote(query)))
        if _is_blocked(result):
            _print_err('Unable to find an answer because the search engine temporarily blocked the request. '
                       'Please wait a few minutes or select a different search engine.')
            raise BlockError("Temporary block by search engine")

        html = pq(result)
        return self._extract_links(html, search_engine)

    def _extract_links_from_bing(self, html):
        html.remove_namespaces()
        return [a.attrib['href'] for a in html('.b_algo')('h2')('a')]

    def _extract_links_from_google(self, html):
        return [a.attrib['href'] for a in html('.l')] or \
            [a.attrib['href'] for a in html('.r')('a')]

    def _extract_links_from_duckduckgo(self, html):
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

    def _extract_links(self, html, search_engine):
        if search_engine == 'bing':
            return self._extract_links_from_bing(html)
        if search_engine == 'duckduckgo':
            return self._extract_links_from_duckduckgo(html)
        return self._extract_links_from_google(html)

    def _get_links_with_cache(self, query):
        cache_key = query + "-links"
        res = cache.get(cache_key)
        if res:
            if res == CACHE_EMPTY_VAL:
                res = False
            return res

        links = self._get_links(query)
        if not links:
            cache.set(cache_key, CACHE_EMPTY_VAL)

        question_links = self._get_questions(links)
        cache.set(cache_key, question_links or CACHE_EMPTY_VAL)

        return question_links

    def _get_answers(self, args):
        """
        @args: command-line arguments
        returns: array of answers and their respective metadata
                False if unable to get answers
        """
        question_links = self._get_links_with_cache(args['query'])
        if not question_links:
            return False

        answers = []
        initial_position = args['pos']
        multiple_answers = (args['num_answers'] > 1 or args['all'])

        for answer_number in range(args['num_answers']):
            current_position = answer_number + initial_position
            args['pos'] = current_position
            link = self.get_link_at_pos(question_links, current_position)
            answer = self._get_answer(args, question_links)
            if not answer:
                continue
            if not args['link'] and not args['json_output'] and multiple_answers:
                answer = ANSWER_HEADER.format(link, answer, STAR_HEADER)
            answer += '\n'
            answers.append({
                'answer': answer,
                'link': link,
                'position': current_position
            })

        return answers

    def get_proxies(self):
        proxies = getproxies()
        filtered_proxies = {}
        for key, value in proxies.items():
            if key.startswith('http'):
                if not value.startswith('http'):
                    filtered_proxies[key] = 'http://%s' % value
                else:
                    filtered_proxies[key] = value
        return filtered_proxies

    def _get_result(self, url):
        pass
        # try:
        #     return howdoi_session.get(url, headers={'User-Agent': _random_choice(USER_AGENTS)},
        #                             proxies=get_proxies(),
        #                             verify=VERIFY_SSL_CERTIFICATE).text
        # except requests.exceptions.SSLError as e:
        #     _print_err('Encountered an SSL Error. Try using HTTP instead of '
        #                'HTTPS by setting the environment variable "HOWDOI_DISABLE_SSL".\n')
        #     raise e

    def extract(self):
        print("Hello extract")
        pass
