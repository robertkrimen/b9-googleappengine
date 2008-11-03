def extract(source, *names):
    result = None
    for name in names:
        value = source.pop( name, None )
        if result is None and value is not None:
            result = value
    return result

def seek(source, *names):
    for name in names:
        if name in source:
            return source[name]
    return None

def empty(value):
    return not(bool(value) or value is 0)

def default(value, default=''):
    return value if not empty( value ) else default

def pluralize(count, singular, plural):
    if count == 1:
        return singular
    else:
        return plural

def percentage(numerator = 0, denominator = 0):
    if denominator == 0:
        return None
    return ( float( numerator ) / float( denominator ) ) * 100

def average(numerator = 0, denominator = 0):
    if denominator == 0:
        return None
    return float(numerator) / float(denominator)

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
