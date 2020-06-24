from howdoi.plugins import BasePlugin

import re
import os
import sys
import appdirs

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

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

BLOCKED_QUESTION_FRAGMENTS = (
    'webself.cache.googleusercontent.com',
)

URL = os.getenv('HOWDOI_URL') or 'stackoverflow.com'


CACHE_EMPTY_VAL = "NULL"
CACHE_DIR = appdirs.user_cache_dir('howdoi')
CACHE_ENTRY_MAX = 128


class StackOverflowPlugin(BasePlugin):
    def format_output(self, code, args):
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

    def search(self, args):
        return self._get_answers(args)

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

    def _get_links(self, query):
        search_engine = os.getenv('HOWDOI_SEARCH_ENGINE', 'google')
        search_url = self._get_search_url(search_engine)

        result = self._get_result(search_url.format(URL, url_quote(query)))
        if self._is_blocked(result):
            _print_err('Unable to find an answer because the search engine temporarily blocked the request. '
                       'Please wait a few minutes or select a different search engine.')
            raise BlockError("Temporary block by search engine")

        html = pq(result)
        return self._extract_links(html, search_engine)

    def _get_links_with_cache(self, query):
        cache_key = query + "-links"
        res = self.cache.get(cache_key)
        if res:
            if res == CACHE_EMPTY_VAL:
                res = False
            return res

        links = self._get_links(query)
        if not links:
            self.cache.set(cache_key, CACHE_EMPTY_VAL)

        question_links = self._get_questions(links)
        self.cache.set(cache_key, question_links or CACHE_EMPTY_VAL)

        return question_links

    def _is_question(self, link):
        for fragment in BLOCKED_QUESTION_FRAGMENTS:
            if fragment in link:
                return False
        return re.search(r'questions/\d+/', link)

    def _get_result(self, url):
        return [{'answer': 'scala> val x = "scala is awesome"\nx: java.lang.String = scala is awesome\n\nscala> x.reverse\nres1: String = emosewa si alacs\n', 'link': 'https://stackoverflow.com/questions/7700399/scala-reverse-string', 'position': 1}]

    def _get_answer(self, args, links):
        link = self.get_link_at_pos(links, args['pos'])
        if not link:
            return False

        cache_key = link
        page = self.cache.get(link)
        if not page:
            page = self._get_result(link + '?answertab=votes')
            self.cache.set(cache_key, page)

        html = pq(page)

        first_answer = html('.answer').eq(0)

        instructions = first_answer.find('pre') or first_answer.find('code')
        args['tags'] = [t.text for t in html('.post-tag')]

        if not instructions and not args['all']:
            text = self.get_text(first_answer.find('.post-text').eq(0))
        elif args['all']:
            texts = []
            for html_tag in first_answer.items('.post-text > *'):
                current_text = self.get_text(html_tag)
                if current_text:
                    if html_tag[0].tag in ['pre', 'code']:
                        texts.append(self._format_output(current_text, args))
                    else:
                        texts.append(current_text)
            text = '\n'.join(texts)
        else:
            text = self._format_output(self.get_text(instructions.eq(0)), args)
        if text is None:
            text = NO_ANSWER_MSG
        text = text.strip()
        return text

    def _get_questions(self, links):
        return [link for link in links if self._is_question(link)]
