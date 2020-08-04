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


class Store:
    def __init__(self, store_dir=DEFAULT_STORE_DIR):
        self._cache = FileSystemCache(store_dir, default_timeout=0)
        if not self._cache.has(Keys.FIRST_INSTALL_DATE):
            self._cache.clear()
            self._cache.set(Keys.FIRST_INSTALL_DATE, datetime.today().strftime("%Y-%m-%d"))

    def __getitem__(self, key):
        return self._cache.get(key)

    def __setitem__(self, key, item):
        self._cache.add(key, item)


class Stats:
    def __init__(self, store):
        self.store = store

    def get_days_since_first_install(self):
        first_install_date = self.store[Keys.FIRST_INSTALL_DATE]
        delta = datetime.today() - datetime.strptime(first_install_date, "%Y-%m-%d")
        return delta.days

    def store_query(self, query):
        pass
