import appdirs

CACHE_EMPTY_VAL = "NULL"

CACHE_DIR = appdirs.user_cache_dir('howdoi')

CACHE_ENTRY_MAX = 128

SUPPORTED_SEARCH_ENGINES = ('google', 'bing', 'duckduckgo')

SUPPORTED_HELP_QUERIES = ['use howdoi', 'howdoi', 'run howdoi',
                          'do howdoi', 'howdoi howdoi', 'howdoi use howdoi']
