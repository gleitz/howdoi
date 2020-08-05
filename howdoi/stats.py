import appdirs
from cachelib import FileSystemCache
from time import time
from datetime import timedelta, datetime
DEFAULT_STORE_DIR = appdirs.user_cache_dir('howdoi-stats')

'''
1. first install

'''


class Keys:
    FIRST_INSTALL_DATE = 'FIRST_INSTALL_DATE'
    HOUR_OF_DAY_PREFIX = 'STATS_HOUR_OF_DAY'
    QUERY_COUNT_PREFIX = 'QUERY_COUNT_PREFIX'


class Stats:
    def __init__(self, cache):
        self.DISALLOWED_WORDS = set(['in', 'a', 'an', 'for', 'on'])
        self.cache = cache
        if not self.cache.has(Keys.FIRST_INSTALL_DATE):
            self.cache.clear()
            self.cache.set(Keys.FIRST_INSTALL_DATE, datetime.today().strftime("%Y-%m-%d"))

    def get_days_since_first_install(self):
        first_install_date = self.cache.get(Keys.FIRST_INSTALL_DATE)
        delta = datetime.today() - datetime.strptime(first_install_date, "%Y-%m-%d")
        return delta.days

    def increment_key(self, key):
        self.cache.inc(key)

    def __getitem__(self, key):
        return self.cache.get(key)

    def process_query_string(self, querystring):
        if not querystring:
            return
        words = querystring.split(" ")
        for word in words:
            word = word.lower()
            if word not in self.DISALLOWED_WORDS:
                self.increment_key(Keys.QUERY_COUNT_PREFIX+word)

    def store_current_hour_of_day(self):
        curr_hour_of_day = datetime.now().hour
        key = Keys.HOUR_OF_DAY_PREFIX + str(curr_hour_of_day)
        self.increment_key(key)

    def process_args(self, args):
        self.store_current_hour_of_day()
        self.process_query_string(args.get('query'))
