howdoi
====================================================

.. image:: http://imgs.xkcd.com/comics/tar.png
        :target: https://xkcd.com/1168/

instant coding answers via the command line
-------------------------------------------

.. image:: https://secure.travis-ci.org/gleitz/howdoi.png?branch=master
        :target: https://travis-ci.org/gleitz/howdoi

.. image:: https://pypip.in/d/howdoi/badge.png
        :target: https://crate.io/packages/howdoi

Are you a hack programmer? Do you find yourself constantly Googling for
how to do basic programing tasks?

Suppose you want to know how to format a date in bash. Why open your browser
and read through blogs (risking major distraction) when you can simply stay
in the console and ask howdoi:

::

    $ howdoi format date bash
    > DATE=`date +%Y-%m-%d`

howdoi will answer all sorts of queries:

::

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

Installation
------------

::

    pip install howdoi

or

::

    pip install git+https://github.com/gleitz/howdoi.git#egg=howdoi

or

::

    brew install https://raw.github.com/gleitz/howdoi/master/howdoi.rb

or

::

    python setup.py install

Usage
-----

::

    usage: howdoi.py [-h] [-p POS] [-a] [-l] [-c] [-n NUM_ANSWERS] QUERY [QUERY ...]

    instant coding answers via the command line

    positional arguments:
      QUERY                 the question to answer

    optional arguments:
      -h, --help            show this help message and exit
      -p POS, --pos POS     select answer in specified position (default: 1)
      -a, --all             display the full text of the answer
      -l, --link            display only the answer link
      -c, --color           enable colorized output
      -n NUM_ANSWERS, --num-answers NUM_ANSWERS
                            number of answers to return
      -C, --clear-cache     clear the cache

Author
------

-  Benjamin Gleitzman (`@gleitz <http://twitter.com/gleitz>`_)


Notes
-----

-  Works with Python2 and Python3
-  A standalone Windows executable with the howdoi application `is available here <https://dl.dropbox.com/u/101688/website/misc/howdoi.exe>`_.
-  An Alfred Workflow for howdoi can be found at `http://blog.gleitzman.com/post/48539944559/howdoi-alfred-even-more-instant-answers <http://blog.gleitzman.com/post/48539944559/howdoi-alfred-even-more-instant-answers>`_.
-  Howdoi uses a cache for faster access to previous questions. Caching functionality can be disabled by setting the HOWDOI_DISABLE_CACHE environment variable. The cache is stored in `~/.cache/howdoi`.
-  You can use HOWDOI_LOCALIZATION environment variable to set the localization of your question. Using this will change the search url to the localization url of your choice. Current supported localizations are **en** and **pt-br**.
-  Special thanks to Rich Jones
   (`@miserlou <https://github.com/miserlou>`_) for the idea.

Troubleshooting
---------------

You might get the following error when installing with Homebrew:

::

    ==> python setup.py install

    http://peak.telecommunity.com/EasyInstall.html

    Please make the appropriate changes for your system and try again.

Fix the error by executing the following command:

::

    sudo chmod -R go+w /Library/Python/2.7/site-packages/
