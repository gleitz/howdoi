from pyquery import PyQuery as pq

from howdoi.howdoi import Plugin
from howdoi.utils import (
    ANSWER_HEADER,
    NO_ANSWER_MSG,
    STAR_HEADER,
    SSLError,
    _clear_cache,
    _format_output,
    _get_cache_key,
    _get_help_instructions,
    _get_links_with_cache,
    _get_result,
    _is_help_query,
    _parse_cmd,
    cache,
    get_link_at_pos,
    get_text,
    get_texts,
)


class StackOverflow(Plugin):
    """Default howdoi plugin that queries StackOverflow.
    """

    def __init__(self):
        super().__init__()
        self.description = "StackOverflow Plugin"

    def _get_answer(self, args, links):
        link = get_link_at_pos(links, args["pos"])
        if not link:
            return False

        cache_key = link
        page = cache.get(link)
        if not page:
            page = _get_result(link + "?answertab=votes")
            cache.set(cache_key, page)

        html = pq(page)

        first_answer = html(".answer").eq(0)

        instructions = first_answer.find("pre") or first_answer.find("code")
        args["tags"] = [t.text for t in html(".post-tag")]

        if not instructions and not args["all"]:
            text = get_text(first_answer.find(".post-text").eq(0))
        elif args["all"]:
            texts = []
            for html_tag in first_answer.items(".post-text > *"):
                current_text = get_text(html_tag)
                if current_text:
                    if html_tag[0].tag in ["pre", "code"]:
                        texts.append(_format_output(current_text, args))
                    else:
                        texts.append(current_text)
            text = "\n".join(texts)
        else:
            text = _format_output(get_text(instructions.eq(0)), args)
        if text is None:
            text = NO_ANSWER_MSG
        text = text.strip()
        return text

    def _get_answers(self, args):
        """
        @args: command-line arguments
        returns: array of answers and their respective metadata
                False if unable to get answers
        """

        question_links = _get_links_with_cache(args["query"])
        if not question_links:
            return False

        answers = []
        initial_position = args["pos"]
        multiple_answers = args["num_answers"] > 1 or args["all"]

        for answer_number in range(args["num_answers"]):
            current_position = answer_number + initial_position
            args["pos"] = current_position
            link = get_link_at_pos(question_links, current_position)
            answer = self._get_answer(args, question_links)
            if not answer:
                continue
            if not args["link"] and not args["json_output"] and multiple_answers:
                answer = ANSWER_HEADER.format(link, answer, STAR_HEADER)
            answer += "\n"
            answers.append(
                {"answer": answer, "link": link, "position": current_position}
            )

        return answers

    def howdoi(self, raw_query, parser, cache):
        args = raw_query
        if type(raw_query) is str:  # you can pass either a raw or a parsed query
            args = vars(parser.parse_args(raw_query.split(" ")))

        args["query"] = " ".join(args["query"]).replace("?", "")
        cache_key = _get_cache_key(args)

        if _is_help_query(args["query"]):
            return _get_help_instructions() + "\n"

        res = cache.get(cache_key)

        if res:
            return _parse_cmd(args, res)

        try:
            res = self._get_answers(args)
            if not res:
                res = {"error": "Sorry, couldn't find any help with that topic\n"}
            cache.set(cache_key, res)
        except (ConnectionError, SSLError):
            return {"error": "Failed to establish network connection\n"}
        finally:
            return _parse_cmd(args, res)
