import time
import pydebug

debug = pydebug.debug('examples:test2')


def hi_there():
    debug("hi there2")


def slow():
    time.sleep(0.1)
    debug('should be milliseconds now')

    time.sleep(1)
    debug('should be seconds now')
