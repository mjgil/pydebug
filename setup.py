#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


setup(name='pydebug',
      version='1.0.3',
      description="Tiny python debugging utility modeled after visionmedia's node.js debug module",
      long_description=desc,
      author='Malcom Gilbert',
      author_email='malcomgilbert@gmail.com',
      url='https://github.com/mjgil/pydebug',
      license='MIT',
      packages=['pydebug']
      )
