import re
import b9

class Parser:

    def __init__(self, map = None, source = None):
        if isinstance(map, basestring):
            _map = {}
            for line in map.splitlines():
                if re.search('^\s*#', line) or re.search('^\s*$', line):
                    continue
                (left, right) = line.split()
                _map[left] = right
            map = _map
        self._map = map
        self._source = source
        self.reset()
        if self._source is not None:
            self.parse()

    def reset(self):
        self._store = {}
        self._valid = None
        self._record = []

    def set(self, key, value):
        self._store[key] = value

    def get(self, key, default = None, none = None, empty = None):
        if key in self._store:
            return self._store[key]
        key = self.map(key)
        value = self._source.get(key, default)
        if empty is not None and b9.empty( value ):
            return empty
        elif none is not None and value is None:
            return none
        else:
            return value

    def parse(self, source = None):
        if source is not None:
            self._source = source
        self._valid = True # Parsing is successful by default
        self.PARSE()

    def map(self, key):
        if self._map is None:
            return key
        return self._map.get(key, key)
    
    def valid(self):
        return True == self._valid

    def invalid(self):
        return False == self._valid

    def error(self, reason):
        self._valid = False
        self._record.append(reason)

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
        return self._parser._record[0]
