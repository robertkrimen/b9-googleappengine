def extract(dict_, *names):
    result = None
    for name in names:
        value = dict_.pop(name, None)
        if result is None and value is not None:
            result = value
    return result

def empty(value):
    return not(bool(value) or value is 0)

def default(value, default=''):
    return value if not empty(value) else default

