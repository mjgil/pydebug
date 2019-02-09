import pydebug

debug = pydebug.debug(__name__)


def hi_there():
    print('hi', __name__)
    debug("hi there 3", __name__)
