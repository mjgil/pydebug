import os
import re

reTrue = re.compile(r'^(yes|on|true|enabled)$', re.IGNORECASE)
reFalse = re.compile(r'^(no|off|false|disabled)$',  re.IGNORECASE)


def inspect_ops():
    """Get options from environment variables
    Any env.variable prefixed with DEBUG_ will be included
    """
    # for key in os.environ.keys():
    keys = [key for key in os.environ.keys()
            if key.lower().startswith('debug_')]
    obj = {}
    for key in keys:
        prop = key[6:].lower()
        val = os.environ.get(key)
        if reTrue.match(val):
            val = True
        elif reFalse.match(val):
            val = False
        elif val == 'null':
            val = None
        else:
            val = int(val, 10)
        obj[prop] = val

    return obj


def load():
    return os.environ.get('DEBUG', '')


def save(namespaces):
    os.environ['DEBUG'] = namespaces
