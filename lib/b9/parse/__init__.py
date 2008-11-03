import re
import logging
import b9
import __builtin__

class Parser:

    def __init__(self, map = None, source = None):
        if isinstance(map, basestring):
            _map = {}
            for line in map.splitlines():
                if re.search('^\s*#', line) or re.search('^\s*$', line):
                    continue
                keys = line.split()
                canonical_key = keys.pop(0)
                keys = __builtin__.map( lambda x: x.replace('%', canonical_key), keys )
                _map[canonical_key] = tuple( keys )
            map = _map
        if map and not len( map ):
            map = None
        self._map = map
        self._source = source
        self.reset()
        if self._source is not None:
            self.parse()

    def map(self, key):
        if self._map is None:
            return [ key ]
        return self._map.get(key, [ key ])

    def _in(self, key, source):
        if key in source:
            return True
        keys = self.map(key)
        for key in keys:
            if key in source:
                return True
        return False

    def _get(self, key, source, none = None, empty = None):
        value = None
        keys = self.map(key)
        for key in keys:
            value = source.get(key)
            if value is not None:
                break
        if empty is not None and b9.empty( value ):
            return empty
        elif none is not None and value is None:
            return none
        else:
            return value
    
    def clear(self):
        self._store = {}

    def reset(self):
        self._store = {}
        self._valid = None
        self._record = []

    def set(self, *given):
        if len( given ) == 1:
            if isinstance( given[0], dict ):
                self._store.update( given[0] )
            else:
                raise NameError, "Don't know what to do"
        else:
            self._store[given[0]] = given[1]

    def fetch(self, key, none = None, empty = None):
        return self._get(key, self._source, none, empty)

    def get(self, key, into = None, none = None, empty = None):
        if key in self._store:
            value = self._store[key]
        else:
            value = self._get(key, self._source, none, empty)
        if value is not None and into is not None:
            return into(value)
        else:
            return value

    def load(self, key, into = None, none = None, empty = None):
        if key in self._store:
            value = self._store[key]
            if into is None:
                return value
        else:
            value = self.fetch(key, none, empty)
        if value is not None and into is not None:
            value = into(value)
        self._store[key] = value
        return value

    def slice(self, keys):
        slice = {}
        if isinstance( keys, basestring ):
            keys = keys.split()
        for key in keys:
            slice[key] = self.get(key)
        return slice

    def have(self, key):
        if key in self._store:
            return True
        return self._in(key, self._source, **given)

    def empty(self, key):
        return b9.empty( self.get(key) )

    def none(self, key):
        return self.get(key) is None

    def parse(self, source = None):
        if source is not None:
            self._source = source
        self._valid = True # Parsing is successful by default
        self.PARSE()

    def valid(self):
        return True == self._valid

    def invalid(self):
        return False == self._valid

    def error(self, reason):
        self._valid = False
        self._record.append(reason)

    def reason(self, ii = 0):
        if not ii < len(self._record):
            return ''
        return self._record[ii]

    def check(self):
        if self._valid is None:
            self.parse()
        if self.invalid():
            raise ParseException, self

    def PARSE(self):
        pass

class ParseException:

    def __init__(self, parser):
        self._parser = parser

    def __str__(self):
        return self._parser.reason()

    def reason(self, ii = 0):
        return self._parser.reason(ii)
        
        
