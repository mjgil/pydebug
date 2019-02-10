import platform
import re
import sys
import time
from typing import Dict, List, Pattern

from colorama import AnsiToWin32

from . import env_helpers

__all__ = ['debug', 'enable']
sep_regex = "[\\s,]+"
colors = [6, 2, 3, 4, 5, 1]

names = []  # type: List[Pattern]
skips = []  # type: List[Pattern]
prev = {}  # type: Dict[str, int]
prevColor = 0

inspect_ops = env_helpers.inspect_ops()
debug_names = env_helpers.load()
use_color = inspect_ops.get('color', True)
hide_date = inspect_ops.get('hide_date', False)


def enable(namespaces):
    env_helpers.save(namespaces)
    split_names = re.split(sep_regex, namespaces)

    names.clear()
    skips.clear()

    for name in split_names:
        if not name:
            # ignore empty strings
            continue
        name = name.replace("*", ".*?")
        if name.startswith("-"):
            skips.append(re.compile("^%s$" % name[1:]))
        else:
            names.append(re.compile("^%s$" % name))


def enabled(name):
    if name.endswith('*'):
        return True
    if any(r.match(name) for r in skips):
        return False
    return any(r.match(name) for r in names)


def color():
    global prevColor
    retval = colors[prevColor % len(colors)]
    prevColor += 1
    return retval


def humanize(us):
    """Turn microseconds into human readable

    Parameters
    ----------
    us : int
        Microseconds

    Returns
    -------
    string
        us as milliseconds, seconds, minutes or hours
    """
    ms = 1000
    sec = 1000 * ms
    min = 60 * sec
    hour = 60 * min

    if us >= hour:
        return "%sh" % round(us/hour, 1)
    if us >= min:
        return "%sm" % round(us/min, 1)
    if us >= sec:
        return "%ss" % round(us/sec, 1)
    if us >= ms:
        return "%sms" % round(us/ms, 1)
    return "%sus" % us


def noop(*args, **kwargs):
    pass


def to_utc_string(input_time):
    return time.strftime("%a, %d %b %Y %T GMT", time.gmtime(input_time))


def debug(name):
    """Creates a debug funtion for a specific namespace

    Parameters
    ----------
    name : string
        Name of the namespace

    Returns
    -------
    function
        function with 'printable' interface to be used for debug logging
    """
    name = name.replace('.', ':')  # enables the use of __name__
    if not enabled(name):
        noop.enabled = False
        return noop

    c = color()
    is_windows = platform.system() == "Windows"

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
        return "  \033[9{0}m{1} \033[3{0}m\033[90m{2}\033[3{0}m +{3}\033[0m" \
            .format(c, name, fmt, humanize(us))

    def plain(fmt, us):
        dt = '' if hide_date else to_utc_string(time.time())
        return "{} {} {} +{}".format(dt, name, fmt, humanize(us))

    def printable(*args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        file = kwargs.get('file', sys.stderr)
        flush = kwargs.get('flush', False)
        show_color = file.isatty() and use_color

        if is_windows and show_color:
            file = AnsiToWin32(sys.stderr)

        us = time_diff()
        fmt = sep.join([repr(x) for x in args])
        fmt = colored(fmt, us) if show_color else plain(fmt, us)

        file.write(fmt+end)
        if flush:
            file.flush()

    printable.enabled = True
    return printable


enable(env_helpers.load())
