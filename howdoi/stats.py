import heapq
import collections
from datetime import datetime, timedelta
from time import time

import appdirs
from termgraph import termgraph
from cachelib import FileSystemCache

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

COLORS = []
ARGS = {'filename': '-', 'title': None, 'width': 50, 'format': '{:<5.1f}', 'suffix': '', 'no_labels': False, 'no_values': False, 'color': None, 'vertical': False, 'stacked': False,
        'histogram': False, 'bins': 5, 'different_scale': False, 'calendar': False, 'start_dt': None, 'custom_tick': '', 'delim': '', 'verbose': False, 'label_before': False, 'version': False}


def draw_horizontal_graph(data, labels, custom_args=None):
    if custom_args is None:
        custom_args = {}

    assert len(data) == len(labels)
    termgraph.chart(COLORS, [[datapoint] for datapoint in data], {
                    **ARGS, **custom_args}, [str(label) for label in labels])


# class StatsReporter:
#     def __init__(self, stats):
#         self.stats = stats

#     def _get_max_from_frequency_map(self, frequency_map):
#         return max(frequency_map, key=lambda k: frequency_map[k])

#     def _get_min_from_frequency_map(self, frequency_map):
#         return min(frequency_map, key=lambda k: frequency_map[k])

#     def report(self):
#         days_since_first_install = self.stats.get_days_since_first_install()


def get_top_n_from_dict(dict_, N):
    top_n = []
    for key in dict_:
        heapq.heappush(top_n, (dict_[key], key))
        if len(top_n) > N:
            heapq.heappop(top_n)
    top_n.sort(reverse=True)
    top_n = [(k, v) for v, k in top_n]
    return top_n


class Stats:
    def __init__(self, cache):
        self.DISALLOWED_WORDS = set(['in', 'a', 'an', 'for', 'on'])
        self.cache = cache
        if not self.cache.has(FIRST_INSTALL_DATE_KEY):
            self.cache.clear()
            self.cache.set(FIRST_INSTALL_DATE_KEY, datetime.today().strftime(DATESTRING_FORMAT))

    def crunch_stats(self):
        # first install days since
        days_since = self.get_days_since_first_install()
        cached_request_count = self[CACHE_HIT_KEY]
        total_request_count = self[TOTAL_REQUESTS_KEY]
        outbound_request_count = total_request_count - cached_request_count
        search_engine_frequency_map = self[SEARCH_ENGINE_KEY]
        max_search_engine_key = max(search_engine_frequency_map,
                                    key=lambda engine: search_engine_frequency_map[engine])

        success = self[SUCCESS_RESULT_KEY]
        failures = self[ERROR_RESULT_KEY]

        hour_of_day_map = self[HOUR_OF_DAY_KEY]

        word_map = self[QUERY_KEY]

        word_key_map = self[QUERY_WORD_KEY]

        print('************* date/time stats *************')
        print('youve been using howdoi for ', days_since, 'days')
        print('avrg queries per day --->', total_request_count//days_since)

        print('******************************************************')

        print('************* requests stats *************')
        draw_horizontal_graph([outbound_request_count*100/total_request_count, cached_request_count*100/total_request_count],
                              ['Outbound Requests', 'Cache Saved Requests'], {'suffix': '%', })

        print('******************************************************')

        print('************* search engine stats *************')

        keys = []
        values = []
        for k in search_engine_frequency_map:
            keys.append(k)
            values.append(search_engine_frequency_map[k])

        print('Your most used search engine is ', max_search_engine_key,
              search_engine_frequency_map[max_search_engine_key])

        draw_horizontal_graph(values, keys, {'suffix': ' uses', 'format': '{:<1d}'})

        print('success/failed requests statistics')
        total = success+failures
        draw_horizontal_graph([success*100/total, failures*100/total], ['Succesful Requests', 'Failed Requests'],
                              {'suffix': '%', })

        # print('hour of day map -->', hour_of_day_map)
        max_key = max(hour_of_day_map, key=lambda hour: hour_of_day_map[hour])
        print('youre most active at', max_key, hour_of_day_map[max_key])

        keys, values = [], []
        for k in hour_of_day_map:
            keys.append(k)
            values.append(hour_of_day_map[k])

        draw_horizontal_graph(values, keys, {'suffix': ' uses', 'format': '{:<1d}'})

        print('*************************************************')
        print('********************query related stats*********************')
        max_key = max(word_map, key=lambda word: word_map[word])
        print('The query you\'ve made the most is "', max_key, '" with ', word_map[max_key], 'occurences')

        max_key = max(word_key_map, key=lambda word: word_key_map[word])
        print('The most common word in your queries is "', max_key, '" with ', word_key_map[max_key], 'occurences')
        print('Here are the top 5 words in your queries')
        top_n = get_top_n_from_dict(word_key_map, 5)
        keys = []
        values = []

        for k, v in top_n:
            keys.append(k)
            values.append(v)

        draw_horizontal_graph(values, keys, {'suffix': ' uses', 'format': '{:<1d}'})

        link_key_map = self[DISCOVERED_LINKS_KEY]
        max_key = max(link_key_map, key=lambda link: link_key_map[link])
        top_n = get_top_n_from_dict(link_key_map, 10)

        print('The most common link you\'ve encountered is "', max_key, '" with ', link_key_map[max_key], 'occurences')
        keys = []
        values = []

        for k, v in top_n:
            keys.append(k)
            values.append(v)

        print('Here are the top 10 links from your queries')
        draw_horizontal_graph(values, keys, {'suffix': ' uses', 'format': '{:<1d}'})

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
