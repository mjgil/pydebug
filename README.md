# pydebug

  Tiny python debugging utility modeled after visionmedia's node.js debug module and the python 3 print function

## Installation

```
$ python setup.py install
```

## Usage

 With `debug` you simply invoke the exported function to generate your debug function, passing it a name which will determine if a noop function is returned, or custom decorated function that emulates the python 3 `print` function but, by default, prints to `sys.stderr`. A unique color is selected per-function for visibility.
 
Example _test.py_:

```py
import pydebug
import time

# 
# pydebug.debug(name)
#
# once you have initialized the debug module you can call it as shown below
#
# debug(*objects, sep=' ', end='\n', file=sys.stderr, flush=False)
#

debug = pydebug.debug("test")
debug("hi there2")

debug2 = pydebug.debug("test2")
debug2("awesome")

debug({"awesome": True}, True, 1, "test")
debug([], {1,2,3}, {"awesome": True}, True, 1, "test")

time.sleep(0.1)
debug('should be milliseconds now')

time.sleep(1)
debug('should be seconds now')
```

 The __DEBUG__ environment variable is then used to enable these based on space or comma-delimited names. Here are some examples:

```
$ DEBUG=* python test_pydebug.py
$ DEBUG=test python test_pydebug.py
$ DEBUG=test2 python test_pydebug.py
$ DEBUG=test* python test_pydebug.py
```

## Microsecond diff

  When actively developing an application it can be useful to see when the time spent between one `debug()` call and the next. Suppose for example you invoke `debug()` before requesting a resource, and after as well, the "+NNNus" will show you how much time was spent between calls.

## When File is not a TTY
  When the file is not a TTY, `to_utc_string()` is called which mimicks the default behavior of the Javascript `Date#toUTCString()` method used in the node.js debug module, making it more useful for logging the debug information as shown below

```
$ DEBUG=* python test_pydebug.py 2>&1 | grep test
$ DEBUG=* python test_pydebug.py 2>&1 | grep test2
```
 
  
## Conventions

 If you're using this in one or more of your libraries, you _should_ use the name of your library so that developers may toggle debugging as desired without guessing names. If you have more than one debuggers you _should_ prefix them with your library name and use ":" to separate features. For example "bodyParser" from Connect would then be "connect:bodyParser". 

## Wildcards

  The "*" character may be used as a wildcard. Suppose for example your library has debuggers named "connect:bodyParser", "connect:compress", "connect:session", instead of listing all three with `DEBUG=connect:bodyParser,connect.compress,connect:session`, you may simply do `DEBUG=connect:*`, or to run everything using this module simply use `DEBUG=*`.

  You can also exclude specific debuggers by prefixing them with a "-" character or whitespace.  For example:

```
$ DEBUG=test2,-test python test_pydebug.py
$ DEBUG="test2 -test" python test_pydebug.py
```

## License 

The MIT License (MIT)

Copyright (c) 2013 Malcom Gilbert

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
