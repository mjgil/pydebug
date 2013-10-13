import os
import re
import sys
import time


__all__ = ['debug']
names = []
skips = []
sep_regex = "[\s,]+"

debug_names = os.environ.get('DEBUG', '')
split_names = re.split(sep_regex, debug_names)

colors = [6, 2, 3, 4, 5, 1]
prev = {}
prevColor = 0

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


def humanize(us):
    ms = 1000
    sec = 1000 * ms
    min = 60 * sec
    hour = 60 * min

    if us >= hour: return "%sh" % round(us/hour, 1)
    if us >= min: return "%sm" % round(us/min, 1)
    if us >= sec: return "%ss" % round(us/sec, 1)
    if us >= ms: return "%sms" % round(us/ms, 1)
    return "%sus" % us


def noop(*args, **kwargs):
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

    def time_diff():
        curr = time.time() * 1000000.0  # float microseconds
        us = curr - prev.get(name, curr)
        prev[name] = curr
        return us

    def colored(fmt, us):
        """
        colors the output,
        mimicks pythons print() function
        """
        return "  \033[9{0}m{1} \033[3{0}m\033[90m{2}\033[3{0}m +{3}\033[0m".format(
               c, name, fmt, humanize(us))

    def plain(fmt, us):
        return "{} {} {} +{}".format(to_utc_string(time.time()),
                                     name, fmt, humanize(us))

    def printable(*args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        file = kwargs.get('file', sys.stderr)
        flush = kwargs.get('flush', False)

        us = time_diff()
        fmt = sep.join([repr(x) for x in args])
        fmt = colored(fmt, us) if file.isatty() else plain(fmt, us)

        file.write(fmt+end)
        if flush:
            file.flush()

    return printable
