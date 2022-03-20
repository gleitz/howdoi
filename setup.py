#!/usr/bin/env python

import glob
import subprocess
from pathlib import Path
from distutils.cmd import Command
from setuptools import setup, find_packages
# pylint: disable=unused-import
import fastentrypoints  # noqa: F401
# pylint: enable=unused-import
import howdoi


class Lint(Command):
    """A custom command to run Flake8 on all Python source files.
    """
    description = 'run Flake8 on Python source files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        local_python_files_str = ' '.join(glob.glob('*.py'))
        commands = {'Flake8': 'flake8 --config=.flake8rc .'.split(),
                    'Pylint': f'pylint howdoi {local_python_files_str} --rcfile=.pylintrc'.split()}

        for linter, command in commands.items():
            try:
                print(f'\nRunning {linter}...')
                subprocess.check_call(command)
                print(f'No lint errors found by {linter}')
            except FileNotFoundError:
                print(f'{linter} not installed')
            except subprocess.CalledProcessError:
                pass


def read(*names):
    values = {}
    for name in names:
        value = ''
        for extension in ('.txt', '.md'):
            filename = name + extension
            if Path(filename).is_file():
                with open(filename) as in_file:  # pylint: disable=unspecified-encoding
                    value = in_file.read()
                break
        values[name] = value
    return values


# pylint: disable=consider-using-f-string
long_description = """
%(README)s

# News

%(CHANGES)s

""" % read('README', 'CHANGES')
# pylint: enable=consider-using-f-string


setup(
    name='howdoi',
    version=howdoi.__version__,
    description='Instant coding answers via the command line',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
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
    extras_require={
        "keep": ["keep],
    },
    entry_points={
        'console_scripts': [
            'keep = keep.cli:cli [keep]'
            'howdoi = howdoi.howdoi:command_line_runner',
        ]
    },
    install_requires=[
        'Pygments',
        'cssselect',
        'lxml',
        'pyquery',
        'requests',
        'cachelib',
        'appdirs',
        'rich'
    ],
    cmdclass={
        'lint': Lint
    }
)
