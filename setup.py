#!/usr/bin/env python

from setuptools import setup, find_packages
import howdoi
import os

def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(name='howdoi',
      version=howdoi.__version__,
      description='A code search tool',
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Documentation",
        ],
      keywords='howdoi help console',
      author='Benjamin Gleitzman',
      author_email='gleitz@mit.edu',
      maintainer='Benjamin Gleitzman',
      maintainer_email='gleitz@mit.edu',
      url='https://github.com/gleitz/howdoi',
      license='MIT',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'howdoi = howdoi.howdoi:command_line_runner',
            ]
        },
      install_requires=[
        'pyquery',
        ],
      )
