import pydebug


debug = pydebug.debug("test")

debug("hi there")
debug("hi there2")

debug2 = pydebug.debug("test2")
debug2("awesome")
debug2("even more awesome")

print 1, 2, 3, 4
debug(1,2,3,4)
