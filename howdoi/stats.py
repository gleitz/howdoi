import collections
from datetime import datetime, timedelta
from time import time

import appdirs
from termgraph import termgraph
from cachelib import FileSystemCache
from howdoi.utils import get_top_n_from_dict, safe_divide

DEFAULT_STORE_DIR = appdirs.user_cache_dir('howdoi-stats')

FIRST_INSTALL_DATE_KEY = 'FIRST_INSTALL_DATE_KEY'
CACHE_HIT_KEY = 'CACHE_HIT_KEY'
TOTAL_REQUESTS_KEY = 'TOTAL_REQUESTS_KEY'
DISCOVERED_LINKS_KEY = 'DISCOVERED_LINKS_KEY'
ERROR_RESULT_KEY = 'ERROR_RESULT_KEY'
SUCCESS_RESULT_KEY = 'SUCCESS_RESULT_KEY'
DATE_KEY = 'DATE_KEY'
HOUR_OF_DAY_KEY = 'HOUR_OF_DAY_KEY'
QUERY_KEY = 'QUERY_KEY'
QUERY_WORD_KEY = 'QUERY_WORD'
DATESTRING_FORMAT = "%Y-%m-%d"
TIMESTRING_FORMAT = "%H:%M:%S"
SEARCH_ENGINE_KEY = 'SEARCH_ENGINE_KEY'
DATETIME_STRING_FORMAT = " ".join((DATESTRING_FORMAT, TIMESTRING_FORMAT))

TERMGRAPH_DEFAULT_ARGS = {'filename': '-', 'title': None, 'width': 50, 'format': '{:<5.1f}', 'suffix': '', 'no_labels': False, 'no_values': False, 'color': None, 'vertical': False, 'stacked': False,
                          'histogram': False, 'bins': 5, 'different_scale': False, 'calendar': False, 'start_dt': None, 'custom_tick': '', 'delim': '', 'verbose': False, 'label_before': False, 'version': False}

Report = collections.namedtuple('Report', ['group', 'content'])


def draw_horizontal_graph(data, labels, custom_args=None):
    assert len(data) == len(labels)
    if custom_args is None:
        custom_args = {}
    termgraph.chart([], [[datapoint] for datapoint in data], {
                    **TERMGRAPH_DEFAULT_ARGS, **custom_args}, [str(label) for label in labels])


class StatsReporter:
    def __init__(self, args, colors=[]):
        self.termgraph_args = args
        self.COLORS = colors
        self._report_group_map = collections.OrderedDict()

    def add(self, report):
        assert isinstance(report, Report)
        if report.group not in self._report_group_map:
            self._report_group_map[report.group] = []

        self._report_group_map[report.group].append(report)

    def render_report(self, report):
        if callable(report.content):
            report.content()
        elif isinstance(report.content, str):
            print(report.content)

    def render_report_separator(self, length, separator_char="*"):
        separation_string = separator_char*length
        print(separation_string)

    def report(self):
        for key in self._report_group_map:
            self.render_report_separator(70)
            for report in self._report_group_map[key]:
                self.render_report(report)


class Stats:
    def __init__(self, cache):
        self.DISALLOWED_WORDS = set(['in', 'a', 'an', 'for', 'on'])
        self.cache = cache
        self.sr = StatsReporter(TERMGRAPH_DEFAULT_ARGS)
        if not self.cache.has(FIRST_INSTALL_DATE_KEY):
            self.cache.clear()
            self.cache.set(FIRST_INSTALL_DATE_KEY, datetime.today().strftime(DATESTRING_FORMAT))

    def load_time_stats(self):
        # TODO - Add heatmap.
        sr = self.sr
        days_since_first_install = self.get_days_since_first_install() or 0
        total_request_count = self[TOTAL_REQUESTS_KEY] or 0

        sr.add(Report(
            'time-related-stats', 'You have been using howdoi for {} days.'.format(days_since_first_install)))

        sr.add(
            Report(
                'time-related-stats', 'You have made an average of {} queries per day.'.format(
                    safe_divide(total_request_count, days_since_first_install))
            )
        )
        hour_of_day_map = self[HOUR_OF_DAY_KEY]

        if total_request_count > 0 and hour_of_day_map:
            most_active_hour_of_day = max(hour_of_day_map, key=lambda hour: hour_of_day_map[hour])

            sr.add(
                Report(
                    'time-related-stats', 'You are most active between {}:00 and {}:00.'.format(
                        most_active_hour_of_day, most_active_hour_of_day+1
                    )
                )
            )

            keys, values = [], []
            for k in hour_of_day_map:
                lower_time_bound = str(k) + ":00"
                upper_time_bound = str(k+1) + ":00" if k+1 < 24 else "00:00"
                keys.append(lower_time_bound + "-" + upper_time_bound)
                values.append(hour_of_day_map[k])

            sr.add(
                Report(
                    'time-related-stats', lambda: draw_horizontal_graph(data=values, labels=keys, custom_args={
                        'suffix': ' uses', 'format': '{:<1d}'})
                )
            )

    def load_request_stats(self):
        sr = self.sr
        total_request_count = self[TOTAL_REQUESTS_KEY] or 0
        cached_request_count = self[CACHE_HIT_KEY] or 0
        total_request_count = self[TOTAL_REQUESTS_KEY] or 0
        outbound_request_count = total_request_count - cached_request_count
        successful_requests = self[SUCCESS_RESULT_KEY] or 0
        failed_requests = self[ERROR_RESULT_KEY] or 0

        sr.add(
            Report('network-request-stats', 'Of the {} requests you have made using howdoi, {} have been saved by howdoi\'s cache'.format(
                total_request_count, cached_request_count))
        )

        sr.add(
            Report('network-request-stats', 'Also, {} requests have succeeded, while {} have failed due to connection issues, or some other problem.'.format(
                successful_requests, failed_requests))
        )

        if total_request_count > 0:
            sr.add(
                Report(
                    'network-request-stats', lambda: draw_horizontal_graph(
                        data=[safe_divide(outbound_request_count*100, total_request_count),
                              safe_divide(cached_request_count*100, total_request_count)],
                        labels=['Outbound Requests', 'Cache Saved Requests'],
                        custom_args={'suffix': '%', }
                    )
                )
            )

        if successful_requests+failed_requests > 0:
            sr.add(
                Report('network-request-stats', lambda: draw_horizontal_graph(
                    data=[safe_divide(successful_requests*100, successful_requests+failed_requests),
                          safe_divide(failed_requests*100, successful_requests+failed_requests)],
                    labels=['Succesful Requests', 'Failed Requests'],
                    custom_args={'suffix': '%', }
                )
                )
            )

    def load_search_engine_stats(self):
        sr = self.sr
        search_engine_frequency_map = self[SEARCH_ENGINE_KEY]
        if search_engine_frequency_map is not None:
            max_search_engine_key = max(search_engine_frequency_map,
                                        key=lambda engine: search_engine_frequency_map[engine])
            sr.add(
                Report(
                    'search-engine-stats', 'Your most used search engine is {}'.format(
                        max_search_engine_key.title()
                    )
                )
            )

            search_engine_keys = []
            search_engine_values = []
            for k in search_engine_frequency_map:
                search_engine_keys.append(k)
                search_engine_values.append(search_engine_frequency_map[k])

            sr.add(
                Report(
                    'search-engine-stats', lambda: draw_horizontal_graph(
                        data=search_engine_values, labels=search_engine_keys, custom_args={'suffix': ' uses', 'format': '{:<1d}'})
                )
            )

    def load_query_related_stats(self):
        sr = self.sr
        query_map = self[QUERY_KEY]
        query_words_map = self[QUERY_WORD_KEY]
        top_5_query_key_vals = get_top_n_from_dict(query_map, 5)

        top_5_query_words_key_vals = get_top_n_from_dict(query_words_map, 5)

        if len(top_5_query_key_vals) > 0:
            most_common_query = top_5_query_key_vals[0][0]
            sr.add(
                Report(
                    'query-stats', 'The query you\'ve made the most times is {}'.format(
                        most_common_query
                    )
                )
            )
        if len(top_5_query_words_key_vals) > 0:
            most_common_query_word = top_5_query_words_key_vals[0][0]
            sr.add(
                Report(
                    'query-stats', 'The most common word in your queries is {}'.format(
                        most_common_query_word
                    )
                )
            )

            sr.add(
                Report(
                    'query-stats', 'Here are the top 5 words in your queries'
                )
            )
            data = [val for _, val in top_5_query_words_key_vals]
            labels = [key for key, _ in top_5_query_words_key_vals]

            sr.add(
                Report('query-stats', lambda: draw_horizontal_graph(data=data, labels=labels,
                                                                    custom_args={'suffix': ' uses', 'format': '{:<1d}'})
                       ))

    def render_stats(self):
        # sr = StatsReporter(TERMGRAPH_DEFAULT_ARGS)

        # days_since_first_install = self.get_days_since_first_install()
        # cached_request_count = self[CACHE_HIT_KEY]
        # total_request_count = self[TOTAL_REQUESTS_KEY]
        # outbound_request_count = total_request_count - cached_request_count
        # search_engine_frequency_map = self[SEARCH_ENGINE_KEY]
        # successful_requests = self[SUCCESS_RESULT_KEY]
        # failed_requests = self[ERROR_RESULT_KEY]
        # hour_of_day_map = self[HOUR_OF_DAY_KEY]
        # query_map = self[QUERY_KEY]
        # query_words_map = self[QUERY_WORD_KEY]

        # max_search_engine_key = max(search_engine_frequency_map,
        #                             key=lambda engine: search_engine_frequency_map[engine])

        # most_active_hour_of_day = max(hour_of_day_map, key=lambda hour: hour_of_day_map[hour])

        # top_5_query_key_vals = get_top_n_from_dict(query_map, 5)
        # most_common_query = top_5_query_key_vals[0][0]

        # top_5_query_words_key_vals = get_top_n_from_dict(query_words_map, 5)
        # most_common_query_word = top_5_query_words_key_vals[0][0]

        self.load_time_stats()
        self.load_request_stats()
        self.load_search_engine_stats()
        self.load_query_related_stats()
        self.sr.report()

    def get_days_since_first_install(self):
        first_install_date = self.cache.get(FIRST_INSTALL_DATE_KEY)
        delta = datetime.today() - datetime.strptime(first_install_date, DATESTRING_FORMAT)
        return delta.days

    def record_cache_hit(self):
        self.cache.inc(CACHE_HIT_KEY)

    def increment_total_requests(self):
        self.cache.inc(TOTAL_REQUESTS_KEY)

    def __getitem__(self, key):
        return self.cache.get(key)

    def add_value_to_stats_count_map(self, key, value):
        stats_map = self.cache.get(key)
        if stats_map is None:
            stats_map = collections.Counter()
        stats_map[value] += 1
        self.cache.set(key, stats_map)

    def process_query_string(self, querystring):
        if not querystring:
            return
        querystring = querystring.strip()
        self.add_value_to_stats_count_map(QUERY_KEY, querystring)

        words = querystring.split(" ")
        for word in words:
            word = word.lower()
            if word not in self.DISALLOWED_WORDS:
                self.add_value_to_stats_count_map(QUERY_WORD_KEY, word)

    def increment_current_date_count(self):
        curr_date_string = datetime.today().strftime(DATESTRING_FORMAT)
        self.add_value_to_stats_count_map(DATE_KEY, curr_date_string)

    def increment_current_hour_of_day_count(self):
        curr_hour_of_day = datetime.now().hour
        self.add_value_to_stats_count_map(HOUR_OF_DAY_KEY, curr_hour_of_day)

    def process_search_engine(self, search_engine):
        if search_engine:
            self.add_value_to_stats_count_map(SEARCH_ENGINE_KEY, search_engine)

    def process_discovered_links(self, links):
        if not links:
            return
        for link in links:
            self.add_value_to_stats_count_map(DISCOVERED_LINKS_KEY, link)

    def process_args(self, args):
        self.increment_total_requests()
        self.process_search_engine(args.get('search_engine'))
        self.increment_current_date_count()
        self.increment_current_hour_of_day_count()
        self.process_query_string(args.get('query'))

    def process_response(self, res):
        key = ERROR_RESULT_KEY if self._is_error_response(res) else SUCCESS_RESULT_KEY
        self.cache.inc(key)

    def _is_error_response(self, res):
        return not res or (type(res) == dict and res.get('error'))
