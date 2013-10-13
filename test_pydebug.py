import pydebug
import time


debug = pydebug.debug("test")

debug("hi there")
debug("hi there2")

debug2 = pydebug.debug("test2")
debug2("awesome")
debug2("even more awesome")

print 1, 2, 3, 4
debug(1,2,3,4)
debug({"test": 1})
debug({"awesome": True}, True, 1, "test")
debug([], {1,2,3}, {"awesome": True}, True, 1, "test")

time.sleep(0.1)
debug('should be milliseconds now')


time.sleep(1)
debug('should be seconds now')