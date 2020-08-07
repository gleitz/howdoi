import collections
from datetime import datetime, timedelta
from time import time

import appdirs
from cachelib import FileSystemCache

DEFAULT_STORE_DIR = appdirs.user_cache_dir('howdoi-stats')

FIRST_INSTALL_DATE_KEY = 'FIRST_INSTALL_DATE_KEY'
CACHE_HIT_KEY = 'CACHE_HIT_KEY'
TOTAL_REQUESTS_KEY = 'TOTAL_REQUESTS_KEY'
DISCOVERED_LINKS_KEY = 'DISCOVERED_LINKS_KEY'
ERROR_RESULT_KEY = 'ERROR_RESULT_KEY'
VALID_RESULT_KEY = 'VALID_RESULT_KEY'
DATE_KEY = 'DATE_KEY'
HOUR_OF_DAY_KEY = 'HOUR_OF_DAY_KEY'
QUERY_KEY = 'QUERY_KEY'
QUERY_WORD_KEY = 'QUERY_WORD'
DATESTRING_FORMAT = "%Y-%m-%d"
TIMESTRING_FORMAT = "%H:%M:%S"
SEARCH_ENGINE_KEY = 'SEARCH_ENGINE_KEY'
DATETIME_STRING_FORMAT = " ".join((DATESTRING_FORMAT, TIMESTRING_FORMAT))


class Stats:
    def __init__(self, cache):
        self.DISALLOWED_WORDS = set(['in', 'a', 'an', 'for', 'on'])
        self.cache = cache
        if not self.cache.has(FIRST_INSTALL_DATE_KEY):
            self.cache.clear()
            self.cache.set(FIRST_INSTALL_DATE_KEY, datetime.today().strftime(DATESTRING_FORMAT))

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
        key = ERROR_RESULT_KEY if self._is_error_response(res) else VALID_RESULT_KEY
        self.cache.inc(key)

    def _is_error_response(self, res):
        return not res or (type(res) == dict and res.get('error'))
