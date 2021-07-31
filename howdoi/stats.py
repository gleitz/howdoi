import collections
from datetime import datetime

# GLOBAL VARIABLES - changes for every object hence made
# store the date for first installation
FIRST_INSTALLED = 'dummy'
# permission for dashboard initially set to true
# if set to true only then send the data to dashboard
DASHBOARD_PERMISSION = True
# redundant words
REDUNDANT_WORDS = ['a', 'an', 'the', 'is', 'for', 'on', 'it', 'in']
# user can choose qny, set by default to index 1
DATESTRING_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"]
# stores the total number of queries done in howdoi
TOTAL_REQUESTS = 'TOTAL_REQUESTS'
SEARCH_ENGINES = "dummy"


# class to show the collected stats
# class RenderStats:
#     def __init__(self):
#         print("inside graph function")


class CollectStats:

    def __init__(self, cache):
        self.cache = cache
        if not self.cache.has(FIRST_INSTALLED):
            self.cache.clear()
            # SET FORMAT TO DEFAULT BUT CAN BE CHANGED BY USER
            self.cache.set(FIRST_INSTALLED, datetime.today().strftime(DATESTRING_FORMATS[0]))

    # to store user's most used search engines
    def search_engine_stats(self, search_engine):
        # print("in search engine fun")
        if search_engine:
            search_engines_storage = self.cache.get(SEARCH_ENGINES)
            if search_engines_storage is None:
                search_engines_storage = collections.Counter()

            search_engines_storage[search_engine] += 1
            # print(search_engines_storage)
            self.cache.set(SEARCH_ENGINES, search_engines_storage)
        print("working")

    # stores the top queries done with howdoi
    # def howdoi_queries_distribution(self):
    #     print("in howdoi usage")

    def increase_key(self, key):
        self.cache.inc(key)

    def increase_days_used(self):
        # function to inc the number of days howdoi was used
        print("working")
        current_date = datetime.today().strftime(DATESTRING_FORMATS[0])
        processed_date = str(current_date)
        self.increase_key(processed_date)

    # check how many times cache was used and how many times servers were pinged
    # def cache_vs_requests_hit(self):
    #     print("in cache vs hits")

    # <-----------------counter functions ------------------------>
    def increase_requests(self):
        # print("increasing requests")
        print("called")
        self.cache.inc(TOTAL_REQUESTS)
        # print(TOTAL_REQUESTS)

    # main runner calling every function
    def run(self, args):
        # task 1 -> increase query counter by 1 since used howdoi
        self.increase_requests()
        self.search_engine_stats(args.get('search_engine'))
        # print("i am working")
