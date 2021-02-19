## Usage

If that's your first time using howdoi, run the quick help

```bash
$ howdoi howdoi
```


Print the help manual
```bash
$ howdoi # "howdoi -h" also prints help

usage: howdoi.py [-h] [-p POS] [-n NUM] [-a] [-l] [-c] [-C] [-j] [-v] [-e [ENGINE]]
                 [--save] [--view] [--remove] [--empty] [QUERY ...]

instant coding answers via the command line

positional arguments:
  QUERY                 the question to answer

optional arguments:
  -h, --help            show this help message and exit
  -p POS, --pos POS     select answer in specified position (default: 1)
  -n NUM, --num NUM     number of answers to return (default: 1)
  -a, --all             display the full text of the answer
  -l, --link            display only the answer link
  -c, --color           enable colorized output
  -C, --clear-cache     clear the cache
  -j, --json            return answers in raw json format
  -v, --version         displays the current version of howdoi
  -e [ENGINE], --engine [ENGINE]
                        search engine for this query (google, bing, duckduckgo)
  --save, --stash       stash a howdoi answer
  --view                view your stash
  --remove              remove an entry in your stash
  --empty               empty your stash

environment variable examples:
  HOWDOI_COLORIZE=1
  HOWDOI_DISABLE_CACHE=1
  HOWDOI_DISABLE_SSL=1
  HOWDOI_SEARCH_ENGINE=google
  HOWDOI_URL=serverfault.com
```
