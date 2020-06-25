import os

import appdirs


def u(x):
    return x


if os.getenv('HOWDOI_DISABLE_SSL'):  # Set http instead of https
    SCHEME = 'http://'
    VERIFY_SSL_CERTIFICATE = False
else:
    SCHEME = 'https://'
    VERIFY_SSL_CERTIFICATE = True

CACHE_EMPTY_VAL = "NULL"

CACHE_DIR = appdirs.user_cache_dir('howdoi')

CACHE_ENTRY_MAX = 128

SUPPORTED_SEARCH_ENGINES = ('google', 'bing', 'duckduckgo')

SUPPORTED_HELP_QUERIES = ['use howdoi', 'howdoi', 'run howdoi',
                          'do howdoi', 'howdoi howdoi', 'howdoi use howdoi']

ANSWER_HEADER = u('{2}  Answer from {0} {2}\n{1}')

STAR_HEADER = u('\u2605')


BLOCK_INDICATORS = (
    'form id="captcha-form"',
    'This page appears when Google automatically detects requests coming from your computer '
    'network which appear to be in violation of the <a href="//www.google.com/policies/terms/">Terms of Service'
)

SEARCH_URLS = {
    'bing': SCHEME + 'www.bing.com/search?q=site:{0}%20{1}&hl=en',
    'google': SCHEME + 'www.google.com/search?q=site:{0}%20{1}&hl=en',
    'duckduckgo': SCHEME + 'duckduckgo.com/?q=site:{0}%20{1}&t=hj&ia=web'
}

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
                'Chrome/19.0.1084.46 Safari/536.5'),
               ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
                'Safari/536.5'), )
