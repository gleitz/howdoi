import os
import re

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

from pyquery import PyQuery as pq
from howdoi.plugins import BasePlugin

URL = os.getenv('HOWDOI_URL') or 'stackoverflow.com'

CACHE_EMPTY_VAL = "NULL"

NO_ANSWER_MSG = '< no answer given >'

BLOCKED_QUESTION_FRAGMENTS = (
    'webself.cache.googleusercontent.com',
)


class StackOverflowPlugin(BasePlugin):
    def _is_question(self, link):
        for fragment in BLOCKED_QUESTION_FRAGMENTS:
            if fragment in link:
                return False
        return re.search(r'questions/\d+/', link)

    def _get_questions(self, links):
        return [link for link in links if self._is_question(link)]

    def _format_output(self, code, args):
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

        return question_links

    def get_answer(self, args, links):
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
