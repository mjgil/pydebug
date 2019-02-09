#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# convert markdown to rst
try:
    import pypandoc
    desc = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    desc = ''

with open('pydebug/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE
    ).group(1)

with open('requirements/base.txt', 'r') as fd:
    requirements = fd.read().strip().split('\n')

setup(
    name='pydebug',
    version=version,
    description=("Tiny python debugging utility modeled after visionmedia's ",
                 "node.js debug module"),
    long_description=desc,
    author='Malcom Gilbert',
    author_email='malcomgilbert@gmail.com',
    url='https://github.com/mjgil/pydebug',
    license='MIT',
    packages=['pydebug'],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
