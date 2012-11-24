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

VERSION = '0.1'

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(name='howdoi',
      version=VERSION,
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
      include_package_data=True,
      install_requires=[
          'pyquery',
      ],
      )
