To begin with howdoi, after installing howdoi, enter the following command:

```
$ howdoi howdoi
```

This will provide with every information you need about working with howdoi and every command/argument that is present in howdoi. For further information about every flag and environment variables type :

```
$ howdoi -h
```

#### Howdoi flags/arguments.

Howdoi comes with a set of predefined flags/arguments which can be set by you as per your choice. You can just type `howdoi -h` in your command line to see each argument and what they do.

**Syntax** : `howdoi [flag/argument] QUERY`

The available arguments currently are listed below:

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

#### Howdoi Environment variables

Howdoi enables the users to put the environment variables of their choice, the currently supported environment variables are :

- **HOWDOI_COLORIZE** : Colorizes the output by default.
- **HOWDOI_SEARCH_ENGINE** : changes the default search engine for StackOverflow links. By default the search engine is google but other supported are : bing, duckduckgo.
- **HOWDOI_URL** : Changes the source url for answers. By default set to : stackoverflow.com. Currently supported here.
- **HOWDOI_DISABLE_CACHE** : Howdoi uses cache for faster access to previously searched questions. If this environment variable is set, the caching functionality will be set. The cache resides in ~/cache/howdoi/.
- **HOWDOI_DISABLE_SSL** : Allows you to disable SSL.
