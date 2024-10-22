- **Howdoi stashing feature** - We agree that sometimes you need to need search results for later and running the same query again and again
  won’t be that feasible. Hence, Howdoi has a stashing feature which allows you to save your query, view the query, delete the saved
  results and even empty the entire stash ! (see keep documentation for more information on stashing). Here is how you can do this:

  - **stashing: howdoi --save QUERY**
  - **viewing:  howdoi --view**
  - **removing: howdoi --remove (will be prompted which answer to delete)**
  - **emptying: howdoi --empty (empties entire stash, will be prompted to confirm)**

- **Shortcuts for your parameters** - You might run the same parameters many times and again, typing them isn’t always the best option. You can use shortcuts for your parameters by using something like:

  ```
  $ alias h='function hdi(){ howdoi $* -c -n 5; }; hdi'
  ```

  And the in your command line, replace your parameters with your alias i.e. h:

  ```
  $ h format date bash
  ```

- **Other uses and aliases** - You can also search other StackExchange properties for answers.

  Example:

  ```
  $ HOWDOI_URL=cooking.stackexchange.com
  $ howdoi make pesto
  ```

  Or use an alias for the same :

  ```
  $ alias hcook='function hcook(){ HOWDOI_URL=cooking.stackexchange.com howdoi $* ; }; hcook'
  $ hcook make pesto
  ```

- **Setting up environment variables** - Howdoi uses some environment variables which can be configured by the user as per his/her choice.
  The following are the environment variables and their usage :

  - HOWDOI_COLORIZE=1 - Colorizes the output produced.
  - HOWDOI_DISABLE_CACHE=1 - Disables the Caching functionality.
    Howdoi uses a cache for faster access to previous questions. The
    cache is stored in ~/.cache/howdoi.
  - HOWDOI_DISABLE_SSL=1 - Disables the SSL certificate.
  - HOWDOI_SEARCH_ENGINE=google - Changes the search engine to your
    preference (default: google, also supported: bing, duckduckgo).
    The -e flag will switch the underlying engine for a single query.
  - HOWDOI_URL=serverfault.com - Changes the source url for answers
    (default: stackoverflow.com, also supported: serverfault.com,
    pt.stackoverflow.com, full list).
