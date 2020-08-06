import appdirs
from cachelib import FileSystemCache
from time import time
from datetime import timedelta, datetime
DEFAULT_STORE_DIR = appdirs.user_cache_dir('howdoi-stats')

FIRST_INSTALL_DATE_KEY = 'FIRST_INSTALL_DATE_KEY'
DATE_KEY_PREFIX = 'DATE_KEY_PREFIX'
HOUR_OF_DAY_KEY_PREFIX = 'HOUR_OF_DAY_KEY_PREFIX'
QUERY_COUNT_PREFIX = 'QUERY_COUNT_PREFIX'
DATESTRING_FORMAT = "%Y-%m-%d"
TIMESTRING_FORMAT = "%H:%M:%S"
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
                self.increment_key(QUERY_COUNT_PREFIX+word)

    def increment_current_date_count(self):
        curr_date_string = datetime.today().strftime(DATESTRING_FORMAT)
        key = DATE_KEY_PREFIX + str(curr_date_string)
        self.increment_key(key)

    def increment_current_hour_of_day_count(self):
        curr_hour_of_day = datetime.now().hour
        key = HOUR_OF_DAY_KEY_PREFIX + str(curr_hour_of_day)
        self.increment_key(key)

    def process_args(self, args):
        self.increment_current_date_count()
        self.increment_current_hour_of_day_count()
        self.process_query_string(args.get('query'))
