You might get the following error when installing with Homebrew:

```bash
==> python setup.py install

http://peak.telecommunity.com/EasyInstall.html

Please make the appropriate changes for your system and try again.
```

Fix the error by executing the following command:
```bash
sudo chmod -R go+w /Library/Python/2.7/site-packages/
```

An official lxml for python 3.3+ for windows has not yet been released. You may get an error while installing.
Try and install an [unofficial binary for lxml](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml).
```
