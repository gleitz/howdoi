<p align="center">
    <a href="https://pypi.python.org/pypi/howdoi">
        <img src="https://www.dropbox.com/s/dk13iy2uoufdwr7/HowDoIcolor512.png?raw=1" alt="Sherlock, your neighborhood command-line sloth sleuth" />
    </a>
</p>
<h1 align="center">howdoi</h1>
<h2 align="center">Instant coding answers via the command line</h2>
<p align="center"><strong>⚡ Never open your browser to look for help again ⚡</strong></p>

<p align="center">
    <a href="https://github.com/gleitz/howdoi/actions?query=workflow%3A%22Python+CI%22"><img src="https://img.shields.io/github/actions/workflow/status/gleitz/howdoi/python.yml?style=plastic&color=78dce8" alt="build status"></a>
    <a href="https://pepy.tech/project/howdoi"><img src="https://img.shields.io/pypi/dm/howdoi?style=plastic&color=ab9df2&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fhowdoi" alt="downloads"></a>
    <a href="https://pypi.python.org/pypi/howdoi"><img src="https://img.shields.io/pypi/pyversions/howdoi.svg?style=plastic&color=ff6188" alt="Python versions"></a>
</p>

------------------------------------------------------------------------

## Introduction to howdoi

Are you a hack programmer? Do you find yourself constantly Googling for
how to do basic programming tasks?

Suppose you want to know how to format a date in bash. Why open your
browser and read through blogs (risking major distraction) when you can
simply stay in the console and ask howdoi:

    $ howdoi format date bash
    > DATE=`date +%Y-%m-%d`

howdoi will answer all sorts of queries:

    $ howdoi print stack trace python
    > import traceback
    >
    > try:
    >     1/0
    > except:
    >     print '>>> traceback <<<'
    >     traceback.print_exc()
    >     print '>>> end of traceback <<<'
    > traceback.print_exc()

    $ howdoi convert mp4 to animated gif
    > video=/path/to/video.avi
    > outdir=/path/to/output.gif
    > mplayer "$video" \
    >         -ao null \
    >         -ss "00:01:00" \  # starting point
    >         -endpos 10 \ # duration in second
    >         -vo gif89a:fps=13:output=$outdir \
    >         -vf scale=240:180

    $ howdoi create tar archive
    > tar -cf backup.tar --exclude "www/subf3" www

[![image](http://imgs.xkcd.com/comics/tar.png)](https://xkcd.com/1168/)

## Installation

    pip install howdoi

or

    brew install howdoi

## Usage

### New to howdoi?

    howdoi howdoi

### RTFM

-   [Introduction and
    installation](http://gleitz.github.io/howdoi/introduction/)
-   [Usage](http://gleitz.github.io/howdoi/usage/)
-   [Contributing to
    howdoi](http://gleitz.github.io/howdoi/contributing_to_howdoi/)
-   [Advanced
    usage](http://gleitz.github.io/howdoi/howdoi_advanced_usage/)
-   [Troubleshooting](http://gleitz.github.io/howdoi/troubleshooting/)

### Commands

    usage: howdoi [-h] [-p POS] [-n NUM] [-a] [-l] [-c] [-x] [-C] [-j] [-v] [-e [ENGINE]]
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
      -x, --explain         explain how answer was chosen
      -C, --clear-cache     clear the cache
      -j, --json            return answers in raw json format
      -v, --version         display the current version of howdoi
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

Using the howdoi stashing feature (for more advanced features view the
[keep documentation](https://github.com/OrkoHunter/keep)).

    stashing: howdoi --save QUERY
    viewing:  howdoi --view
    removing: howdoi --remove (will be prompted which answer to delete)
    emptying: howdoi --empty (empties entire stash, will be prompted to confirm)

As a shortcut, if you commonly use the same parameters each time and
don\'t want to type them, add something similar to your .bash_profile
(or otherwise). This example gives you 5 colored results each time.

    alias h='function hdi(){ howdoi $* -c -n 5; }; hdi'

And then to run it from the command line simply type:

    $ h format date bash

You can also search other [StackExchange
properties](https://stackexchange.com/sites#traffic) for answers:

    HOWDOI_URL=cooking.stackexchange.com howdoi make pesto

or as an alias:

    alias hcook='function hcook(){ HOWDOI_URL=cooking.stackexchange.com howdoi $* ; }; hcook'
    hcook make pesto

Other useful aliases:

    alias hless='function hdi(){ howdoi $* -c | less --raw-control-chars --quit-if-one-screen --no-init; }; hdi'

## Integrations

-   Slack integration available through
    [slack-howdoi](https://github.com/ellisonleao/slack-howdoi)
-   Telegram integration available through
    [howdoi-telegram](https://github.com/aahnik/howdoi-telegram)
-   Discord integration available through
    [discord-howdoi](https://github.com/MLH-Fellowship/0.5.1-howDoIDiscord)
-   Emacs integration available through
    [emacs-howdoi](https://blog.gleitzman.com/post/700738401851277312/howdoi-use-howdoi-in-emacs)
-   VSCode integration available on the
    [marketplace](https://marketplace.visualstudio.com/items?itemName=howdoi-org.howdoi)
-   Alfred integration available through
    [alfred-howdoi](https://github.com/gleitz/alfred-howdoi)

## Contributors

-   Benjamin Gleitzman ([\@gleitz](http://twitter.com/gleitz))
-   Yanlam Ko ([\@YKo20010](https://github.com/YKo20010))
-   Diana Arreola ([\@diarreola](https://github.com/diarreola))
-   Eyitayo Ogunbiyi ([\@tayoogunbiyi](https://github.com/tayoogunbiyi))
-   Chris Nguyen ([\@chrisngyn](https://github.com/chrisngyn))
-   Shageldi Ovezov ([\@ovezovs](https://github.com/chrisngyn))
-   Mwiza Simbeye
    ([\@mwizasimbeye11](https://github.com/mwizasimbeye11))
-   Shantanu Verma ([\@SaurusXI](https://github.com/SaurusXI))
-   Sheza Munir ([\@ShezaMunir](https://github.com/ShezaMunir))
-   Jyoti Bisht ([\@joeyouss](https://github.com/joeyouss))
-   And [more!](https://github.com/gleitz/howdoi/graphs/contributors)

## How to contribute

We welcome contributions that make howdoi better and improve the
existing functionalities of the project. We have created a separate
[guide to contributing to
howdoi](http://gleitz.github.io/howdoi/contributing_to_howdoi/) that explains
how to get up and running with your first pull request.

## Notes

-   Works with Python 3.7 and newer. Unfortunately Python 2.7 support
    has been discontinued :(
-   Special thanks to Rich Jones
    ([\@miserlou](https://github.com/miserlou)) for the idea
-   More thanks to [Ben Bronstein](https://benbronstein.com/) for the
    logo
