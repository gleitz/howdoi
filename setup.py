#!/usr/bin/env python

from setuptools import setup, find_packages
import howdou
import os

#try:
#    from pypandoc import convert
#    read_md = lambda f: convert(f, 'rst')
#except ImportError:
#    print("warning: pypandoc module not found, could not convert Markdown to RST")
#    read_md = lambda f: open(f, 'r').read()

def extra_dependencies():
    import sys
    ret = []
    if sys.version_info < (2,7):
        ret.append('argparse')
    return ret

def read(*names):
    values = dict()
    extensions = ['.txt', '.md']
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

""" % read('README')

setup(
    name='howdou',
    version=howdou.__version__,
    description='Instant coding answers via the command line',
    #long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Documentation",
    ],
    keywords='howdou help console command line answer',
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='https://github.com/chrisspen/howdou',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'howdou = howdou.howdou:command_line_runner',
        ]
    },
    install_requires=[
        'pyquery',
        'pygments',
        'requests',
        'requests-cache',
        'elasticsearch#>=1.0.0',
        'PyYAML==3.10',
        'python-dateutil>=2.2',
    ] + extra_dependencies(),
)
