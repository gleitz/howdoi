howdoi
======

instant coding answers via the command line
-------------------------------------------

.. image:: https://img.shields.io/travis/gleitz/howdoi?style=plastic&color=78dce8
        :target: https://travis-ci.org/gleitz/howdoi

.. image:: https://img.shields.io/badge/dynamic/json?style=plastic&color=ab9df2&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fhowdoi
        :target: https://pepy.tech/project/howdoi

.. image:: https://img.shields.io/pypi/pyversions/howdoi.svg?style=plastic&color=ff6188
        :target: https://pypi.python.org/pypi/howdoi

|

.. image:: http://sublimate.org/flyers/HowDoIcolor512.png
        :target: https://pypi.python.org/pypi/howdoi
        :alt: Sherlock, your neighborhood sloth sleuth

Sherlock, your neighborhood sloth sleuth.

----

Are you a hack programmer? Do you find yourself constantly Googling for
how to do basic programming tasks?

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

.. image:: http://imgs.xkcd.com/comics/tar.png
        :target: https://xkcd.com/1168/

Installation
------------

::

    pip install howdoi

or

::

    pip install git+https://github.com/gleitz/howdoi.git#egg=howdoi

or

::

    python setup.py install

New to howdoi?
--------------

::

    howdoi howdoi

Usage
-----

::

    usage: howdoi.py [-h] [-p POS] [-a] [-l] [-c] [-j] [-n NUM_ANSWERS] [-C] [-v] [-e ENGINE] [--save] [--view] [--remove] [--empty] QUERY [QUERY ...]

    instant coding answers via the command line

    positional arguments:
      QUERY                 the question to answer

    optional arguments:
      -h, --help            show this help message and exit
      -p POS, --pos POS     select answer in specified position (default: 1)
      -a, --all             display the full text of the answer
      -l, --link            display only the answer link
      -c, --color           enable colorized output
      -j, --json-output     return answers in raw json format, to pretty print try 'howdoi pretty print json command line'
      -n NUM_ANSWERS, --num-answers NUM_ANSWERS
                            number of answers to return
      -C, --clear-cache     clear the cache
      -v, --version         displays the current version of howdoi
      -e ENGINE, --engine ENGINE  change search engine for this query only. Currently supported engines: google (default), bing, duckduckgo.
      --save                stash a howdoi answer
      --view                view your stash
      --remove              remove an entry in your stash
      --empty               empty your stash

Using the howdoi stashing feature (for more advanced features view the `keep documentation <https://github.com/OrkoHunter/keep>`_).

::

    stashing: howdoi --save QUERY
    viewing: howdoi --view
    removing: howdoi --remove (will be prompted which one to delete)
    emptying: howdoi --empty (empties entire stash, will be prompted to confirm)

As a shortcut, if you commonly use the same parameters each time and don't want to type them, add something similar to your .bash_profile (or otherwise). This example gives you 5 colored results each time.

::

    alias h='function hdi(){ howdoi $* -c -n 5; }; hdi'

And then to run it from the command line simply type:

::

    $h this is my query for howdoi

Contributors
------------

-  Benjamin Gleitzman (`@gleitz <http://twitter.com/gleitz>`_)
-  Yanlam Ko (`@YKo20010 <https://github.com/YKo20010>`_)
-  Diana Arreola (`@diarreola <https://github.com/diarreola>`_)
-  Eyitayo Ogunbiyi (`@tayoogunbiyi <https://github.com/tayoogunbiyi>`_)
-  Chris Nguyen (`@chrisngyn <https://github.com/chrisngyn>`_)
-  Shageldi Ovezov (`@ovezovs <https://github.com/chrisngyn>`_)
-  Mwiza Simbeye (`@mwizasimbeye11 <https://github.com/mwizasimbeye11>`_)
-  And `more! <https://github.com/gleitz/howdoi/graphs/contributors>`_

Notes
-----

-  Works with Python2 and Python3
-  There is a `GUI that wraps howdoi <https://pypi.org/project/pysimplegui-howdoi/>`_.
-  There is a `Flask webapp that wraps howdoi <https://howdoi.maxbridgland.com>`_.
-  An Alfred Workflow for howdoi can be found at `http://blog.gleitzman.com/post/48539944559/howdoi-alfred-even-more-instant-answers <http://blog.gleitzman.com/post/48539944559/howdoi-alfred-even-more-instant-answers>`_.
-  Slack integration available through `slack-howdoi <https://github.com/ellisonleao/slack-howdoi>`_.
-  Howdoi uses a cache for faster access to previous questions. Caching functionality can be disabled by setting the HOWDOI_DISABLE_CACHE environment variable. The cache is stored in `~/.cache/howdoi`.
-  You can set the HOWDOI_URL environment variable to change the source url for answers (default: `stackoverflow.com`, also supported: `serverfault.com`, `pt.stackoverflow.com`, `full list <http://stackexchange.com/sites?view=list#traffic>`_).
-  You can set the HOWDOI_SEARCH_ENGINE environment variable to change the underlying search engine for StackOverflow links (default: `google`, also supported: `bing`, `duckduckgo`). The -e flag will switch the underlying engine for a single query.
-  Setting the HOWDOI_COLORIZE environment variable will colorize the output by default.
-  Special thanks to Rich Jones (`@miserlou <https://github.com/miserlou>`_) for the idea.
-  More thanks to `Ben Bronstein <https://benbronstein.com/>`_ for the logo.

Development
-----------

-  Checkout the repo
-  Run ``python -m howdoi.howdoi QUERY`` (if you try running ``python howdoi/howdoi.py`` you might get ``ValueError: Attempted relative import in non-package``).

If you would like to use howdoi from within a python script, just pass your query to `howdoi.howdoi()`:
::

    from howdoi import howdoi

    query = "for loop python"
    output = howdoi.howdoi(query)


Or parse it yourself (either work):

::

    from howdoi import howdoi

    query = "for loop python"
    parser = howdoi.get_parser()
    args = vars(parser.parse_args(query.split(' ')))

    output = howdoi.howdoi(args)

Extension Development
---------------------

To simplify the process of integrating howdoi as a code editor extension, edit the files within the `extension/code-editor-integration folder <https://github.com/gleitz/howdoi/tree/master/extension/code-editor-integration>`_.

To improve upon the Visual Studio Code howdoi extension, edit the files within the `extension/vscode-ext folder <https://github.com/gleitz/howdoi/tree/master/extension/vscode-howdoi>`_ and republish the extension.

Code Editor Integration
~~~~~~~~~~~~~~~~~~~~~~~

Head over to the `README.md <https://github.com/gleitz/howdoi/blob/master/extension/code-editor-integration/README.md>`_ for an in depth explanation on beginning development for the howdoi code editor integration plug-in.

Visual Studio Code Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To begin development for the Visual Studio Code extension, install all necessary packages:

::

    npm install

Then, precompile the extension:

::

    npm run precompile

To run and test the extension, utilize Visual Studio Code's `debugging tools <https://code.visualstudio.com/api/get-started/your-first-extension>`_.

Visual Studio Code Extension Installation
-----------------------------------------

howdoi can now be installed as an extension on Visual Studio Code! There are two ways to install it:

1. On the Visual Studio Code MarketPlace:
-  (coming soon)

2. Directly from the packaged extension:
 - To locally install the howdoi Visual Studio Code package, head over `here <https://github.com/gleitz/howdoi/tree/master/extension/vscode-pkg/README.md>`_.

Contributing
------------

I'm happy to accept pull requests that make howdoi better. If you're thinking of contributing and want a little feedback before you jump into the codebase, post an `issue <https://github.com/gleitz/howdoi/issues>`_ on Github.

Before PRs are accepted they must pass all `Travis tests <https://travis-ci.org/gleitz/howdoi>`_ and not have any flake8 or pylint warnings or errors. This projects uses vanilla configuration files for both linters (``.flake8rc`` and ``.pylintrc`` in the root directory), but with a max line length of 119.

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


An official lxml for python 3.3+ for windows has not yet been released. You may get an error while installing.
Try and install an unofficial binary for lxml from

::

    http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
