## Contributing to Howdoi

As beginners, navigating the codebase and finding your way out of the documentation can become difficult. This page will help you understand everything about contributing to howdoi and the best practices in open source as well.
You can either contribute code to Howdoi (explained on this page) or contribute documentation (explained on next page)

### Setting up the development environment

Follow the page [Setting up the development environment](http://gleitz.github.io/howdoi/development_env/) for setting up the development environment for Howdoi.

### Finding your first issue

- Go to issues in the [howdoi repo](https://github.com/gleitz/howdoi).
- Find the issues which you might be interested to work on. Or, you can also come up with your own ideas of improving howdoi.
- After finding the issue you are interested in : If the issue is an existing one, comment on the issue and ask for it to be assigned to you. Or, if the issue is unlisted and new , create a new issue and fill every information needed in the issues template provided by howdoi and ask for it to be assigned to you.

- After receiving confirmation, start working on the issue and whenever and wherever help is needed, comment on the issue itself describing your query in detail.
- A good guide on how to collaborate efficiently can be found [here](https://lab.github.com/githubtraining/introduction-to-github){:target="\_blank"}.

### Making a Pull request (PR)

- After you have worked on the issue and fixed it, we need to merge it from your forked repository into the howdoi repository. This is done by making a PR.
- You can search
  ```
  howdoi create a pull request on Github
  ```
  in your command line and follow the steps written in it.
- Each PR made should pass all the tests and should not have any flake8 or pylint errors. Github runs tests on each PR but we before that, you should run `python setup.py lint` which will run pylint and flake8.

- Once your commit passes all the tests, make a PR and wait for it to be reviewed and merged.

### Asking for help

At times, help is needed while solving the issue. We recommend the following step for asking for help when you get stuck:

1. Read from howdoi docs and howdoi github to see if your answer has already been answered.
2. Comment on the issue you are working describing in detail what problems you are facing.
3. Make sure to write your query in detail and if it is bug, include steps to reproduce it.
4. If you are not working on any issue and have a question to be answered, open a new issue on Github and wait for a reply on it.

## General guidelines

Be sure to go through these items before creating a new issue:

1. Check the [existing issues](https://github.com/gleitz/howdoi/issues) to see if anyone is already working or have already worken on your issue or a similar one.

2. If there are no current or past issues similar to yours, be sure to give a a **complete description** when creating it.

3. Wait for feedback on the issue before starting to work.

!!! tip
    Include instructions on how to reproduce the bug you found or specific use cases of a requested feature.

!!! Note
    Follow Github's [guide to collaborating efficiently](https://lab.github.com/githubtraining/introduction-to-github).

### Setting up development environment

Clone the git repository
```bash
$ git clone https://github.com/gleitz/howdoi.git
```

Setup and activate a virtual environment
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install packages
```bash
$ pip install -r requirements.txt
```

### Running howdoi

Run on the command-line
```bash
python -m howdoi QUERY
```

!!! note
    If you try running `python howdoi/howdoi.py` (without `-m`) you might get `ValueError: Attempted relative import in non-package`.

If you want to use howdoi from within a python script, just pass your query to `howdoi.howdoi()`

```python
from howdoi import howdoi

query = "for loop python"
output = howdoi.howdoi(query)
```

Or parse it yourself and passed the arguments to `howdoi.howdoi()`
```python
from howdoi import howdoi

query = "for loop python"
parser = howdoi.get_parser()
args = vars(parser.parse_args(query.split(' ')))

output = howdoi.howdoi(args)
```

!!! attention
    Parsing queries yourself is the older way to pass in queries and may be deprecated in the future. Prefer the first example.

### Submitting Pull Requests
Before PRs are accepted they must pass all [Travis tests](https://travis-ci.org/gleitz/howdoi) and not have any `flake8` or `pylint` warnings or errors.

#### Testing
Howdoi uses python's [`unittest`](https://docs.python.org/3/library/unittest.html) library for unit testing. Run the unit tests locally

```bash
$ python -m test_howdoi
```

It's also possible to run only specific tests

```bash
$ python -m unittest test_howdoi.TestClass.test_method
```

Make sure all tests pass before submitting a PR.

!!! tip
    Remmember to run the tests while inside the virtual environment (run `source .venv/bin/activate` to activate it).

#### Linting
Run linting locally with [`flake8`](https://flake8.pycqa.org/en/latest/)
```bash
$ flake8
```
Or [`pylint`](https://www.pylint.org/)
```bash
$ pylint *
```

!!! tip
    Howdoi uses vanilla configuration files for both linters (`.flake8rc` and `.pylintrc` in the root directory), but with a max line length of 119 characters.

## Contributing to Documentation

If you would like to improve the existing documentation, you can do so by using `mkdocs`. Howdoi uses mkdocs to render its documentation. Steps to contribute to docs:

- Every step from [Contributing to howdoi](http://gleitz.github.io/howdoi/contributing_to_howdoi/) remains the same with additional requirements of installing and building mkdocs.
- First, install mkdocs by running the following command:
  ```
  pip install mkdocs
  ```
- You can learn about mkdocs usage from [mkdocs documentation](https://www.mkdocs.org/user-guide/).
- You can propose your documentation by [creating a new issue](https://github.com/gleitz/howdoi/issues/new/choose).
- Once approved in the issue, you can create a PR with modifications to the mkdocs markdown.
- Next, create a new branch and go to the folder `howdoi/docs/` and add a .md file.
- Go to `mkdocs.yml` and add the name of your added .md file in `nav`
- To see the changes in your local server, go to your terminal and in this directory run :

```
   $ mkdocs build
   $ mkdocs serve
```

- Once done, make a PR for the same and wait for it to be reviewed.

## Documentation

To get started building the docs first download `mkdocs`

```bash
$ pip install mkdocs-material markdown-include
```

### Commands

* `python -m mkdocs new [dir-name]` - Create a new project.
* `python -m mkdocs serve` - Start the live-reloading docs server.
* `python -m mkdocs build` - Build the documentation site.
* `python -m mkdocs help` - Print this help message.

### Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

### Here are some example alerts you can use
These are from the [Adomonition](https://python-markdown.github.io/extensions/admonition/) extension

!!! attention
    attention alert

!!! caution
    caution alert

!!! warning
    warning alert

!!! danger
    danger alert

!!! error
    error alert

!!! hint
    hint alert

!!! important
    important alert

!!! tip
    tip alert

!!! note
    note alert

!!! Custom alert
    Custom alert

Alternatively you can use the `!!! type "Custom Title"` format to get the correct type emoji and use any title you want like so:

!!! tip "Tip type alert but with a custom title"
    they're good aren't they

### Include source code in 1 line of code

To import code we can use this syntax inside of a code block with the language label:  "{\!path/to/file\!}".

Here's `../howdoi/__init__.py`

```Python
{!../howdoi/__init__.py!}
```

### Here is a choice tab
Proper syntax highlighted code blocks in these don't work the way you'd think and I don't know how to get them to work normally without some extension

=== "Python"
    To do x in python use this code:

    ```python
    def main():
        print("Hello world")
    if __name__ == "__main__":
        main()
    ```

=== "Golang"
    To do x in golang use this code:

    ```go
    package main
    import "fmt"
    func main() {
        fmt.Println("Hello world")
    }
    ```

You can include the contents of a file
```Python
{!../howdoi/__init__.py!}
```
