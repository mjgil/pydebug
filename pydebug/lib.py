# import termcolor
import os
import re
import sys
import time
# import colorama


__all__ = ['debug']
names = []
skips = []
sep_regex = "[\s,]+"

debug_names = os.environ.get('DEBUG', '')
split_names = re.split(sep_regex, debug_names)

colors = [6, 2, 3, 4, 5, 1]
prev = {}
prevColor = 0
isatty = sys.stdout.isatty()

for name in split_names:
    name = name.replace("*", ".*?")
    if name.startswith("-"):
        skips.append(re.compile("^%s$" % name[1:]))
    else:
        names.append(re.compile("^%s$" % name))


def color():
    global prevColor
    retval = colors[prevColor % len(colors)]
    prevColor += 1
    return retval


def humanize(microsec):
    ms = 1000
    sec = 1000 * ms
    min = 60 * sec
    hour = 60 * min

    return "%s microseconds" % microsec


def noop():
    pass


def to_utc_string(input_time):
    return time.strftime("%a, %d %b %Y %T GMT", time.gmtime(input_time))


def debug(name):
    should_skip = any(r.match(name) for r in skips)

    if should_skip:
        return noop

    has_match = any(r.match(name) for r in names)

    if not has_match:
        return noop

    c = color()

    def colored(fmt):
        curr = time.time() * 1000000  # microseconds
        us = curr - prev.get(name, curr)
        prev[name] = curr

        fmt = """
              \u001b[9{0}m{1} \u001b[3{0}m\u001b[90m
              {2}\u001b[3{0}m +{3}\u001b[0m
              """.format(c, name, fmt, humanize(us))

        sys.stderr.write(fmt)

    def plain(fmt):
        fmt = "{} {} {}".format(to_utc_string(time.time()),
                                name, fmt)

        sys.stderr.write(fmt)

    return colored if isatty else plain

    return name
