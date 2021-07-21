If you would like to improve the existing docs/ add new ideas in docs, you can do so by using mkdocs. Howdoi uses mkdocs to host its documentation. Steps to contribute to docs:

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
