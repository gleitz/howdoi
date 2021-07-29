from time import time
from datetime import datetime, timedelta
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
TOTAL_REQUESTS = 'dummy'
SEARCH_ENGINES = "dummy"

# class to show the collected stats
class RenderStats:
    def __init__(self):
        print("inside graph function")
    
# class to collect stats
class CollectStats:
    # constructor 
    def __init__(self, cache):
        self.cache = cache
        # if this is the first time howdoi is installed
        if not self.cache.has(FIRST_INSTALLED):
            self.cache.clear()
            # SET FORMAT TO DEFAULT BUT CAN BE CHANGED BY USER
            self.cache.set(FIRST_INSTALLED, datetime.today().strftime(DATESTRING_FORMATS[0]))
            
    # to store user's most used search engines
    def search_engine_stats(self):
        print("in search engine fun")
        # frequency = 0
        # if frequency not None :
        #     maximum_frequency  = max(frequency,)
        
    # stores the top queries done with howdoi
    def howdoi_queries_distribution(self):
        print("in howdoi usage")
        
    # check how many times cache was used and how many times servers were pinged
    def cache_vs_requests_hit(self):
        print("in cache vs hits")

    # <-----------------counter functions ------------------------>
    def increase_requests(self):
        print("increasing requests")
    
    # main runner calling every function
    def run(self, args):
        # task 1 -> increase query counter by 1 since used howdoi
        self.increase_requests()
        # print("i am working")
    
    
