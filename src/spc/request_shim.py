from __future__ import absolute_import


class RequestShim(object):
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        return self._data.get(name)

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        self._data[name] = value

    def __delitem__(self, name):
        del self._data[name]

    def get(self, name, default=None):
        return self._data.get(name, default)

    def getlist(self, name):
        return self._data.getlist(name)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data
