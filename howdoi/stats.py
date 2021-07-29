# importing appdirs as howdoi uses it 
import appdirs
from cachelib import FileSystemCache
from time import time
from datetime import *

DEFAULT_DIR = appdirs.user_cache_dir('howdoi-local-stats')


# GLOBAL VARIABLES - changes for every object hence made
# store the date for first installation
FIRST_INSTALLED = 'dummy'
# permission for dashboard initially set to true
# if set to true only then send the data to dashboard
DASHBOARD_PERMISSION = True
# a check for checking redundant words
REDUNDANT_WORDS = ['a','an','the','is','for','on','it','in']


# class to collect stats
class CollectStats:
    # needed functions
    # constructor 
    def __init__(self):
    # to show user his/her most used search engines
    def search_engine_stats():
        
    # stores the number of queries done with howdoi
    def howdoi_usage_stats():

    # check how many times cache was used and how many times servers were pinged
    def cache_vs_requests_hit():
# class to show the collected stats
class RenderStats:
    
    
