import pydebug

debug = pydebug.debug('examples:test1')


def hi_there():
    debug("hi there")


def awesome():
    debug({"test": 1})
    debug({"awesome": True}, True, 1, "test")
    debug([], {1, 2, 3}, {"awesome": True}, True, 1, "test")
