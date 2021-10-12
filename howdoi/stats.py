import collections
from datetime import datetime
from termgraph import termgraph
from .utils import get_top_n_key_val_pairs_from_dict, safe_divide
import sys
# GLOBAL VARIABLES - changes for every object hence made
# store the date for first installation
FIRST_INSTALLED = 'dummy'
# permission for dashboard initially set to true
# if set to true only then send the data to dashboard
DASHBOARD_PERMISSION = True
# redundant words
REDUNDANT_WORDS = ['a', 'an', 'the', 'is', 'for', 'on', 'it', 'in']
HOUR_OF_DAY_KEY = 'DUMMY'
QUERY_WORD_KEY = 'dummy'

SUCCESS_RESULT_KEY = 'dummy'
# user can choose qny, set by default to index 1
DATESTRING_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"]
# stores the total number of queries done in howdoi
TOTAL_REQUESTS = 'TOTAL_REQUESTS'
SEARCH_ENGINES = "dummy"
# aid in checking for the process links and checking its frequency
PROCESSED_LINKS = "processed links"
CACHE_HITS = "CACHE_HITS"
# variabe for checking if res is errored
ERROR_IN_RES = "ERROR_IN_RES"
# variable for checking if the res is not errored
VALID_RES = "VALID_RES"
# class to show the collected stats
# class RenderStats:
#     def __init__(self):
#         print("inside graph function")
QUERY_KEY = "query key"
WORD_OF_QUERY = "WORD OF QUERY"

ERROR_RESULT_KEY= 'dummy'

# ----------------------------> termgraph DEPENDENCIES
TERMGRAPH_DEFAULT_ARGS = {'filename': '-', 'title': None, 'width': 50, 'format': '{:<5.1f}', 'suffix': '', 'no_labels': False, 'no_values': False, 'color': None, 'vertical': False, 'stacked': False,
                          'histogram': False, 'bins': 5, 'different_scale': False, 'calendar': False, 'start_dt': None, 'custom_tick': '', 'delim': '', 'verbose': False, 'label_before': False, 'version': False}

Report = collections.namedtuple('Report', ['group', 'content'])


def draw_graph(data, labels, custom_args = None):
    if sys.version>= '3.6':
        # create graph using the folloing logic
        assert len(data) == len(labels)
        if custom_args is None:
            custom_args = {}
        args = {}
        args.update(TERMGRAPH_DEFAULT_ARGS)
        args.update(custom_args)
        termgraph.chart([], [[datap] for datap in data], args, [str(label) for label in labels])
# ---------------------------------------->

class RenderStats:

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

class CollectStats:

    def __init__(self, cache):
        self.cache = cache
        self.rs = RenderStats(TERMGRAPH_DEFAULT_ARGS)
        if not self.cache.has(FIRST_INSTALLED):
            self.cache.clear()
            # SET FORMAT TO DEFAULT BUT CAN BE CHANGED BY USER
            self.cache.set(FIRST_INSTALLED, datetime.today().strftime(DATESTRING_FORMATS[0]))

    def load_time_stats(self):
        # get termgraph object instance
        rs = self.rs
        
        days_since_first_install = self.get_days_since_first_install() or 0
        total_request_count = self[TOTAL_REQUESTS] or 0

        #  add total time howdoi was used
        rs.add(Report('Time stats', 'You have been using howdoi for {}'.format(days_since_first_install)))
        
        # add termgraph information about time stats
        rs.add(Report('Time stats', 'The average queires made by your are {}'.format(safe_divide(total_request_count, days_since_first_install))))
        
        hour_of_day_map = self[HOUR_OF_DAY_KEY]
        
        if total_request_count > 0 and hour_of_day_map:
            most_active_hour_of_the_day = max(hour_of_day_map, key = lambda hour: hour_of_day_map[hour])

            rs.add(Report('Time stats', 'You are most active between {}:00 and {}:00'.format(most_active_hour_of_the_day,               most_active_hour_of_the_day+1)))
        
            keys, values = [], []
            for k in hour_of_day_map:
                lower_time_bound = str(k) + ":00"
                upper_time_bound = str(k+1) + ":00" if k+1<24 else "00:00"
                keys.append(lower_time_bound+"-"+upper_time_bound)
                values.append(hour_of_day_map[k])
            
            rs.add(
                Report(
                    'time-related-stats', lambda: draw_graph(data=values, labels=keys, custom_args={
                        'suffix': ' uses', 'format': '{:<1d}'})
                )
            )

    def render_search_engine_stats(self):
        
        rs = self.rs
        search_engine_frequency = SEARCH_ENGINES
        if search_engine_frequency is not None:
            max_search_engine = max(search_engine_frequency, key= lambda engine : search_engine_frequency[engine])
            rs.add(Report('Search-engine=stats', 'Your most used search engine is {}'.format(max_search_engine.title())))

        se_keys = []
        se_values = []
        # get values for search engine : get stats
        for i in search_engine_frequency:
            se_keys.append(i)
            se_values.append(search_engine_frequency[i])

        # now add those values to the termgraph
        
        rs.add(Report('search-engine-stats'), lambda :
            draw_graph(
                data = se_values,
                labels = se_keys, custom_args = {'suffix':'uses', 'format':'{:<1d}'}
            ))

    def render_query_stats(self):
        rs = self.rs 
        # get your keys
         
        query_map = self[QUERY_KEY]
        
        # get the map of queries
        query_words_map = self[QUERY_WORD_KEY]
        
        # get the top 5 since we are concerned with those 
        top_5_query_key_vals = get_top_n_key_val_pairs_from_dict(query_map, 5)

        top_5_query_words_key_vals = get_top_n_key_val_pairs_from_dict(query_words_map, 5)

        if len(top_5_query_key_vals) > 0:
            most_common_query = top_5_query_key_vals[0][0]
            rs.add(
                Report(
                    'query-stats', 'The query you\'ve made the most times is {}'.format(
                        most_common_query
                    )
                )
            )
        if len(top_5_query_words_key_vals) > 0:
            most_common_query_word = top_5_query_words_key_vals[0][0]
            rs.add(
                Report(
                    'query-stats', 'The most common word in your queries is {}'.format(
                        most_common_query_word
                    )
                )
            )

            data = [val for _, val in top_5_query_words_key_vals]
            labels = [key for key, _ in top_5_query_words_key_vals]

            rs.add(
                Report('query-stats', lambda: draw_graph(data=data, labels=labels,
                                                                    custom_args={'suffix': ' uses', 'format': '{:<1d}'})
                       ))
    # to store user's most used search engines
    # def search_engine_stats(self, search_engine):
    #     # print("in search engine fun")
    #     if search_engine:
    #         search_engines_storage = self.cache.get(SEARCH_ENGINES)
    #         if search_engines_storage is None:
    #             search_engines_storage = collections.Counter()

    #         search_engines_storage[search_engine] += 1
    #         # print(search_engines_storage)
    #         self.cache.set(SEARCH_ENGINES, search_engines_storage)
    #     print("working")

    # stores the top queries done with howdoi
    # def howdoi_queries_distribution(self):
    #     print("in howdoi usage")

    def render_request_stats(self):
        rs = self.rs
        
        
        total_request_count = self[TOTAL_REQUESTS] or 0
        
        
        cached_request_count = self[CACHE_HITS] or 0
        
        
        total_request_count = self[TOTAL_REQUESTS] or 0
        
        
        outbound_request_count = total_request_count - cached_request_count
        
        
        successful_requests = self[SUCCESS_RESULT_KEY] or 0
        failed_requests = self[ERROR_RESULT_KEY] or 0

        rs.add(
            Report('Network Stats', 'Of the {} requests you have made using howdoi, {} have been saved by howdoi\'s cache'.format(
                total_request_count, cached_request_count))
        )

        rs.add(
            Report('Network Stats', 'Also, {} requests have succeeded, while {} have failed due to connection issues, or some other problem.'.format(
                successful_requests, failed_requests))
        )

        if total_request_count > 0:
            rs.add(
                Report(
                    'network-request-stats', lambda: draw_graph(
                        data=[safe_divide(outbound_request_count*100, total_request_count),
                              safe_divide(cached_request_count*100, total_request_count)],
                        labels=['Outbound Requests', 'Cache Saved Requests'],
                        custom_args={'suffix': '%', }
                    )
                )
            )

        if successful_requests+failed_requests > 0:
            rs.add(
                Report('network-request-stats', lambda: draw_graph(
                    data=[safe_divide(successful_requests*100, successful_requests+failed_requests),
                          safe_divide(failed_requests*100, successful_requests+failed_requests)],
                    labels=['Succesful Requests', 'Failed Requests'],
                    custom_args={'suffix': '%', }
                )
                )
            )


    # main fuction for termgraph stats
    def render_stats(self):
        print("RENDERING STATS, to disable : howdoi --disable_stats")
        self.render_search_engine_stats()
        self.load_time_stats()
        self.render_query_stats()
        self.render_request_stats()
        self.rs.render()
        
    def increase_cache_hits(self):
        self.cache.inc(CACHE_HITS)

    def increase_key(self, key):
        self.cache.inc(key)

    def increase_days_used(self):
        # function to inc the number of days howdoi was used
        print("working")
        current_date = datetime.today().strftime(DATESTRING_FORMATS[0])
        processed_date = str(current_date)
        self.increase_key(processed_date)

    def increase_hours_used(self):
        current_hour = datetime.now().hour
        processed_hour = str(current_hour)
        self.increase_key(processed_hour)
    # check how many times cache was used and how many times servers were pinged
    # def cache_vs_requests_hit(self):
    #     print("in cache vs hits")

    # <-----------------counter functions ------------------------>
    def increase_requests(self):
        # print("increasing requests")
        print("called")
        self.cache.inc(TOTAL_REQUESTS)
        # print(self.cache)

    def process_response(self, res):
        # checking for error in respomnse
        ans = ""
        # check for errored response
        if not res or (isinstance(res, dict) and res.get('error')):
            ans = ERROR_IN_RES
        else:
            ans = VALID_RES
        self.cache.inc(ans)

    def process_links(self, question_links):
        print("processing links ")
        if not question_links:  # checking for empty links
            return
        links_storage = self.cache.get(PROCESSED_LINKS)
        if links_storage is None:
            links_storage = collections.Counter()
            # increase freq by 1 of the processed link
        for i in question_links:
            links_storage[i] += 1
            self.cache.set(PROCESSED_LINKS, links_storage)
    
    def create_storage(self, key, value):
        map_storage = self.cache.get(key)
        if map_storage is None:
            map_storage = collections.Counter()
            
        map_storage[value]+=1
        self.cache.set(key, map_storage)

    def process_user_query(self, query):
        if not query:
            return 
        query = query.strip()
        query_storage = self.cache.get(QUERY_KEY)
        if query_storage is None:
            query_storage = collections.Counter()  

        query_storage[query]+=1
        self.cache.set(QUERY_KEY, query_storage)
        tokens = query.split(" ")
        for token in tokens:
            token  = token.lower()
            if token not in REDUNDANT_WORDS:
                self.create_storage(WORD_OF_QUERY, token)

    # main runner calling every function
    def run(self, args):
        # task 1 -> increase query counter by 1 since used howdoi
        self.increase_requests()
        self.increase_days_used()
        self.search_engine_stats(args.get('search_engine'))
        # print("i am working")
        self.increase_hours_used()
        self.process_user_query(args.get('query'))
