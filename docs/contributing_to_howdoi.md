As beginners, navigating the codebase and finding your way out of the documentation can become difficult. This page will help you understand everything about contributing to howdoi and the best practices in open source as well.
You can either contribute code to Howdoi (explained on this page) or contribute documentation (explained on next page)

#### Setting up the development environment

Follow the page [Setting up the development environment](http://gleitz.github.io/howdoi/development_env/) for setting up the development environment for Howdoi.

#### Finding your first issue

- Go to issues in the [howdoi repo](https://github.com/gleitz/howdoi).
- Find the issues which you might be interested to work on. Or, you can also come up with your own ideas of improving howdoi.
- After finding the issue you are interested in : If the issue is an existing one, comment on the issue and ask for it to be assigned to you. Or, if the issue is unlisted and new , create a new issue and fill every information needed in the issues template provided by howdoi and ask for it to be assigned to you.

- After receiving confirmation, start working on the issue and whenever and wherever help is needed, comment on the issue itself describing your query in detail.
- A good guide on how to collaborate efficiently can be found [here](https://lab.github.com/githubtraining/introduction-to-github){:target="\_blank"}.

#### Making a Pull request (PR)

- After you have worked on the issue and fixed it, we need to merge it from your forked repository into the howdoi repository. This is done by making a PR.
- You can search
  ```
  howdoi create a pull request on Github
  ```
  in your command line and follow the steps written in it.
- Each PR made should pass all the tests and should not have any flake8 or pylint errors. Github runs tests on each PR but we before that, you should run `python setup.py lint` which will run pylint and flake8.

- Once your commit passes all the tests, make a PR and wait for it to be reviewed and merged.

#### Asking for help

At times, help is needed while solving the issue. We recommend the following step for asking for help when you get stuck:

1. Read from howdoi docs and howdoi github to see if your answer has already been answered.
2. Comment on the issue you are working describing in detail what problems you are facing.
3. Make sure to write your query in detail and if it is bug, include steps to reproduce it.
4. If you are not working on any issue and have a question to be answered, open a new issue on Github and wait for a reply on it.
