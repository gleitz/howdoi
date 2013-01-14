howdoi - a code search tool
===========================

Are you a hack programmer? Do you find yourself constantly Googling for
how to do basic programing tasks?

Suppose you want to know how to format a date in bash. Why open your
browser and read through blogs when you can just...

::

    $ howdoi format string bash
    > [foo@bar ~]$date --date "2012-02-13" +%s
    > 1329055200
    > [foo@bar ~]$date --date @1329055200
    > Mon Feb 13 00:00:00 EST 2012
    > [foo@bar ~]$date --date @1329055200 +"%Y-%m-%d"
    > 2012-02-13

howdoi will answer all sorts of queries

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

    brew install https://raw.github.com/gleitz/howdoi/master/howdoi.rb

or

::

    python setup.py install

Usage
-----

::

    howdoi [-h] [-p POS] [-a] [-l] QUERY [QUERY ...]

    code search tool

    positional arguments:
      QUERY              the question to answer

    optional arguments:
      -h, --help         show this help message and exit
      -p POS, --pos POS  select answer in specified position (default: 1)
      -a, --all          display the full text of the answer
      -l, --link         display only the answer link

Author
------

-  Benjamin Gleitzman (`@gleitz <http://twitter.com/gleitz>`_)


Notes
-----

-  Requires Python <= 2.7 (pull requests for a Python 3 version certainly accepted)
-  Requires `PyQuery <http://pypi.python.org/pypi/pyquery>`_
-  A Windows executable with the howdoi application `is available here <https://dl.dropbox.com/u/101688/website/misc/howdoi.exe>`_.
-  Special thanks to Rich Jones
   (`@miserlou <https://github.com/miserlou>`_) for the idea

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
