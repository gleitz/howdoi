#!/usr/bin/env python

from setuptools import setup, find_packages
import fastentrypoints
import howdoi
import os

def extra_dependencies():
    import sys
    return ['argparse'] if sys.version_info < (2, 7) else []


def read(*names):
    values = dict()
    for name in names:
        value = ''
        for extension in ('.txt', '.rst'):
            filename = name + extension
            if os.path.isfile(filename):
                with open(filename) as in_file:
                    value = in_file.read()
                break
        values[name] = value
    return values


long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='howdoi',
    version=howdoi.__version__,
    description='Instant coding answers via the command line',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Documentation",
    ],
    keywords='howdoi help console command line answer',
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
        'Pygments>=2.6.1',
        'argparse>=1.4.0',
        'cssselect>=1.1.0',
        'lxml>=4.5.2',
        'pyquery>=1.4.1',
        'requests>=2.24.0',
        'cachelib>=0.1.1',
        'appdirs>=1.4.4',
        'keep>=2.9',
    ] + extra_dependencies(),
)
