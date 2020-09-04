import os
import sys
import appdirs
from cachelib import FileSystemCache, NullCache

# Handle imports for Python 2 and 3
if sys.version < "3":
    import codecs
    from urllib import quote as url_quote
    from urllib import getproxies
    from urlparse import urlparse, parse_qs

    # Handling Unicode: http://stackoverflow.com/a/6633040/305414
    def u(x):
        return codecs.unicode_escape_decode(x)[0]


else:
    from urllib.request import getproxies
    from urllib.parse import quote as url_quote, urlparse, parse_qs

    def u(x):
        return x


if os.getenv("HOWDOI_DISABLE_SSL"):  # Set http instead of https
    SCHEME = "http://"
    VERIFY_SSL_CERTIFICATE = False
else:
    SCHEME = "https://"
    VERIFY_SSL_CERTIFICATE = True

SUPPORTED_SEARCH_ENGINES = ("google", "bing", "duckduckgo")

URL = os.getenv("HOWDOI_URL") or "stackoverflow.com"

USER_AGENTS = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) "
        "Chrome/19.0.1084.46 Safari/536.5"
    ),
    (
        "Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46"
        "Safari/536.5"
    ),
)
SEARCH_URLS = {
    "bing": SCHEME + "www.bing.com/search?q=site:{0}%20{1}&hl=en",
    "google": SCHEME + "www.google.com/search?q=site:{0}%20{1}&hl=en",
    "duckduckgo": SCHEME + "duckduckgo.com/?q=site:{0}%20{1}&t=hj&ia=web",
}

BLOCK_INDICATORS = (
    'form id="captcha-form"',
    "This page appears when Google automatically detects requests coming from your computer "
    'network which appear to be in violation of the <a href="//www.google.com/policies/terms/">Terms of Service',
)

BLOCKED_QUESTION_FRAGMENTS = ("webcache.googleusercontent.com",)

STAR_HEADER = u("\u2605")
ANSWER_HEADER = u("{2}  Answer from {0} {2}\n{1}")
NO_ANSWER_MSG = "< no answer given >"

CACHE_EMPTY_VAL = "NULL"
CACHE_DIR = appdirs.user_cache_dir("howdoi")
CACHE_ENTRY_MAX = 128

HTML_CACHE_PATH = "cache_html"
SUPPORTED_HELP_QUERIES = [
    "use howdoi",
    "howdoi",
    "run howdoi",
    "do howdoi",
    "howdoi howdoi",
    "howdoi use howdoi",
]

# variables for text formatting, prepend to string to begin text formatting.
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
UNDERLINE = "\033[4m"
END_FORMAT = "\033[0m"  # append to string to end text formatting.

# stash options
STASH_SAVE = "save"
STASH_VIEW = "view"
STASH_REMOVE = "remove"
STASH_EMPTY = "empty"


if os.getenv("HOWDOI_DISABLE_CACHE"):
    cache = NullCache()  # works like an always empty cache
else:
    cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)
