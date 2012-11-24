from setuptools import setup, find_packages
import os

def read(*names):
    values = dict()
    for name in names:
        filename = name + '.txt'
        if os.path.isfile(filename):
            value = open(name + '.txt').read()
        else:
            value = ''
        values[name] = value
    return values

VERSION = '0.1dev'

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README.txt', 'CHANGES.txt')

setup(name='howdoi',
      version=VERSION,
      description='A code search tool',
      long_description=long_description,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        ],
      keywords='howdoi help',
      author='Benjamin Gleitzman',
      author_email='gleitz@mit.edu',
      maintainer='Benjamin Gleitzman',
      maintainer_email='gleitz@mit.edu',
      url='https://github.com/gleitz/howdoi',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'pyquery',
      ],
      )
