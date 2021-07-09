howdoi
======

instant coding answers via the command line
-------------------------------------------

.. image:: https://img.shields.io/github/workflow/status/gleitz/howdoi/Python%20CI?style=plastic&color=78dce8
        :target: https://github.com/gleitz/howdoi/actions?query=workflow%3A%22Python+CI%22

.. image:: https://img.shields.io/badge/dynamic/json?style=plastic&color=ab9df2&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fhowdoi
        :target: https://pepy.tech/project/howdoi

.. image:: https://img.shields.io/pypi/pyversions/howdoi.svg?style=plastic&color=ff6188
        :target: https://pypi.python.org/pypi/howdoi

|

.. image:: http://sublimate.org/flyers/HowDoIcolor512.png
        :target: https://pypi.python.org/pypi/howdoi
        :alt: Sherlock, your neighborhood command-line sloth sleuth

Sherlock, your neighborhood command-line sloth sleuth.

----

### Table of Contents
- Inroduction to howdoi
- Getting started with howdoi
    - Installation 
    - Learning how to use howdoi
    - Howdoi documentation
    - Howdoi extension
- Howdoi documentation
- Contributors
- Contributing to howdoi
- Notes and important points

## INTRODUCTION TO HOWDOI

Howdoi is an open-source command line tool which parses the data on the web and makes the most relevant data available to you in your command line. 
As programmers, we often find ourselves Googling for basic programming tasks. 
For example, you just want to know **“how do you print hello in python”**. You would go and open your browser and read blogs (risking major distraction). With howdoi, you can get the most relevant and correct answers in your command line. 

You just need to type ```howdoi print in python``` and there you have your answer in your command line!.

### GETTING STARTED WITH HOWDOI
All you need is Python 3.5 and above and pip installed to run howdoi in your local system.
**Note : Howdoi Python 2.7 support is discontinued.**

#### Installation
To get started with howdoi, In your command line simply type :
```pip install howdoi```
Or 
```pip install git+https://github.com/gleitz/howdoi.git#egg=howdoi```
Or if you want to use setup tools, you can type:
```python setup.py install```
#### Learning how to use howdoi
To see all the howdoi commands which you can use, simply type:
```howdoi howdoi```
And all the present commands will be shown in front of you. 

#### Understanding howdoi usage
- Howdoi arguments/ flags - Howdoi comes with a set of predefined flags/arguments which can be set by you as per your choice. You can just type ```howdoi -h``` in your command line to see each argument and what they do. The available arguments currently are listed below:
 **- h, --help** : To see the help message which has all the information about every command
**-p POS, --pos POS** : To select answer in any specified position.
**-n NUM, --num NUM** : Defines the number of answers to return. By default, set to 1.
**-a, --all**: Shows the full text of an answer
**-l, --link**: Displays only the link of the answer
**-j** : Displays the answer in JSON format. Useful when you are building on top of howdoi.
**-c, --color**: Prints colorized output
**-x, --explain**: Explains why the outputted answer was shown to you
**-C, --clear-cache**: Clears the cache
**-j, --json** : Outputs the answer in raw JSON format
**-v, --version**: Displays your current version of howdoi.
**-e [ENGINE], --engine [ENGINE]** : Allows to choose the search engine for the query. Currently supported - google, bing, duckduckgo
**--save, --stash** : Enables stashing feature for a howdoi answer
**--view** : Displayed the stash 
**--remove** : Removes an entry in your stash
**--empty** : Empties the stash completely

- Howdoi stashing feature - We agree that sometimes you need to need search results for later and running the same query again and again won’t be that feasible. Hence, Howdoi has a stashing feature which allows you to save your query, view the query, delete the saved results and even empty the entire stash ! (see keep documentation for more information on stashing). Here is how you can do this:
**stashing: howdoi --save QUERY**
**viewing:  howdoi --view**
**removing: howdoi --remove (will be prompted which answer to delete)**
**emptying: howdoi --empty (empties entire stash, will be prompted to confirm)**

- Shortcuts for your parameters - You might run the same parameters many times and again, typing them isn’t always the best option. You can use shortcuts for your parameters by using something like:
```alias h='function hdi(){ howdoi $* -c -n 5; }; hdi'```
And the in your command line, replace your parameters with your alias i.e. h:
```h format date bash```

- Other uses and aliases- You can also search other StackExchange properties for answers. Example:
```HOWDOI_URL=cooking.stackexchange.com```
```howdoi make pesto```
Or use an alias for the same :
```alias hcook='function hcook(){ HOWDOI_URL=cooking.stackexchange.com howdoi $* ; }; hcook'```
```hcook make pesto```

- Setting up environment variables : Howdoi uses some environment variables which can be configured by the user as per his/her choice. The following are the environment variables and their usage :
    - HOWDOI_COLORIZE=1 - Colorizes the output produced.
    - HOWDOI_DISABLE_CACHE=1 -  Disables the Caching functionality. Howdoi uses a cache for faster access to previous questions. The cache is stored in ~/.cache/howdoi.
    - HOWDOI_DISABLE_SSL=1 - Disables the SSL certificate.
    - HOWDOI_SEARCH_ENGINE=google - Changes the search engine to your preference (default: google, also supported: bing, duckduckgo). The -e flag will switch the underlying engine for a single query.
    - HOWDOI_URL=serverfault.com - Changes the source url for answers (default: stackoverflow.com, also supported: serverfault.com, pt.stackoverflow.com, full list).


#### Howdoi documentation
The howdoi documentation lies [here](https://gleitz.github.io/howdoi/) and is hosted in the form of mkdocs. It contains each and every detail about howdoi and its related things. The mkdocs also reside in the folder ```howdoi/docs/```
Contents of Howdoi Documentation :
- Introduction and Installing 
- Usage of howdoi
- Setting up the development environemnt
- How to contribute
- Contributing documentation
- Developing extension
- Troubleshooting

### CONTRIBUTORS

-  Benjamin Gleitzman (`@gleitz <http://twitter.com/gleitz>`_)
-  Yanlam Ko (`@YKo20010 <https://github.com/YKo20010>`_)
-  Diana Arreola (`@diarreola <https://github.com/diarreola>`_)
-  Eyitayo Ogunbiyi (`@tayoogunbiyi <https://github.com/tayoogunbiyi>`_)
-  Chris Nguyen (`@chrisngyn <https://github.com/chrisngyn>`_)
-  Shageldi Ovezov (`@ovezovs <https://github.com/chrisngyn>`_)
-  Mwiza Simbeye (`@mwizasimbeye11 <https://github.com/mwizasimbeye11>`_)
-  Shantanu Verma (`@SaurusXI <https://github.com/SaurusXI>`_)
-  And `more! <https://github.com/gleitz/howdoi/graphs/contributors>`_

### HOW TO CONTRIBUTE
We welcome contributions that make Howdoi better and/or improve the existing functionalities of the project. We have created a separate guide to contributing to howdoi which resides in the howdoi documentation in mkdcos. The guide contains the following:
- Introduction for first time contributors
- Getting started with howdoi 
- Making PRs and testing 
- Asking for help

### NOTES AND IMPORTANT POINTS
-  Works with Python 3.5 and newer. Unfortunately Python 2.7 support has been discontinued :(
-  There is a `GUI that wraps howdoi <https://pypi.org/project/pysimplegui-howdoi/>`_.
-  There is a `Flask webapp that wraps howdoi <https://howdoi.maxbridgland.com>`_.
-  An Alfred Workflow for howdoi can be found at `http://blog.gleitzman.com/post/48539944559/howdoi-alfred-even-more-instant-answers <http://blog.gleitzman.com/post/48539944559/howdoi-alfred-even-more-instant-answers>`_.
-  Slack integration available through `slack-howdoi <https://github.com/ellisonleao/slack-howdoi>`_.
-  Telegram integration available through `howdoi-telegram <https://github.com/aahnik/howdoi-telegram>`_.
-  Special thanks to Rich Jones (`@miserlou <https://github.com/miserlou>`_) for the idea.
-  More thanks to `Ben Bronstein <https://benbronstein.com/>`_ for the logo.
