howdoi - a unix code search tool
========================

Are you a hack programmer? Do you find yourself constantly Googling for how to do basic programing tasks?

Suppose you want to know how to format a date in bash. Why open your browser and read through blogs when you can just...

    $ howdoi format string bash
    > date +"%m-%d-%y"

    $ howdoi print stack trace python
    > traceback.print_exc()

    $ howdoi create tar
    > tar -cf backup.tar --exclude "www/subf3" www

Usage:

`howdoi query`

Extra notes:

*   Requires [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
*   Special thanks to Rich Jones ([@miserlou](https://github.com/miserlou)) for the idea

TODOs:

*   Pick the longest code block instead of the first
*   Flag for printing multiple answers instead of the first
*   Flag for displaying the entire answer
*   Flag for retrieving the page URL
