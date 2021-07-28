- Clone the Howdoi repository:

  ```
  $ git clone https://github.com/gleitz/howdoi.git
  ```

- To see how to set up the development for Windows, see [here](http://gleitz.github.io/howdoi/windows-contributing/).

- Setup and activate a virtual environment

  ```
  $ python3 -m venv .venv
  $ source .venv/bin/activate
  ```

- Install all the required packages

  ```
  $ pip install -r requirements.txt
  ```

- Run howdoi

- Running from command line :

  ```
  $ python -m howdoi QUERY
  ```

- Running from a python script : Go to your script in howdoi.howdoi() and pass your query in the argument.

```
from howdoi import howdoi
query = "for loop python"
output = howdoi.howdoi(query)
```

Or , parse it yourself and then pass the arguments:

```
from howdoi import howdoi
query = "for loop python"
parser = howdoi.get_parser()
args = vars(parser.parse_args(query.split(' ')))
output = howdoi.howdoi(args)
```

#### Notes :

- **Parsing queries yourself is the older way to pass in queries and may be deprecated in the future. Prefer the first example.**
- **If you try running python howdoi/howdoi.py (without -m) you might get ValueError: Attempted relative import in non-package.**
