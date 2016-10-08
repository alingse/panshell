#coding=utf-8
#author@alingse
#2016.10.07

from setuptools import setup, find_packages

from codecs import open
import os
import sys

from panshell import VERSION

# Based on https://github.com/pypa/sampleproject/blob/master/setup.py
# and https://python-packaging-user-guide.readthedocs.org/

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

with open(os.path.join(here, 'LICENSE'), encoding='utf-8') as f:
    license = f.read()
    

setup(
    name='panshell',
    version=VERSION,
    description='shell for baidu yunpan',
    long_description=readme,
    author='alingse',
    author_email='alingse@foxmail.com',
    license=license,
    packages=find_packages(exclude=['tests','docs']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "pansh = panshell.core:pansh"
        ]
    }
)
