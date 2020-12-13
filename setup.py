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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
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
        'Pygments',
        'cssselect',
        'lxml',
        'pyquery',
        'requests',
        'cachelib==0.1',
        'appdirs',
        'keep',
    ] + extra_dependencies(),
)
