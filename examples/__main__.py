"""Main of the 'examples' module
run with ``python3 -m examples``
"""
import pydebug
from . import test1, test2, test3

debug = pydebug.debug('examples:main')

print('tada')
debug('start processing')
test1.hi_there()
test2.hi_there()
test3.hi_there()

print(1, 2, 3, 4)
debug(1, 2, 3, 4)

test1.awesome()

test2.slow()

debug(dir([]), repr([]), str([]))

print('Done!')
