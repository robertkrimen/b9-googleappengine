def extract(dict_, *names):
    result = None
    for name in names:
        value = dict_.pop( name, None )
        if result is None and value is not None:
            result = value
    return result

def empty(value):
    return not(bool(value) or value is 0)

def default(value, default=''):
    return value if not empty( value ) else default

def pluralize(count, singular, plural):
    if count == 1:
        return singular
    else:
        return plural

def minute_second_millisecond(millisecond_time):
    millisecond = int( millisecond_time % 1000 )
    second = int( millisecond_time / 1000 ) % 60
    minute = int( millisecond_time / (60 * 1000) )
    clock = "%02d:%02d.%03d" % ( minute, second, millisecond )
    return {
        "clock": clock,
        "millisecond": millisecond,
        "second": second,
        "minute": minute,
    }
