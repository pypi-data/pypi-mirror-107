from collections import MutableMapping
from pprint import pformat
from typing import Iterator, Any


class Field(dict):
    pass


class BaseItem(MutableMapping):

    def __init__(self):
        self._values = {}
        self.fields = getattr(self, 'fields', {})
        for n in dir(self):
            v = getattr(self, n)
            if isinstance(v, Field):
                self.fields[n] = v

    def __getitem__(self, key) -> Any:
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __delitem__(self, key):
        del self._values[key]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator:
        return iter(self._values)

    def __repr__(self):
        return pformat(dict(self))


class Item(BaseItem):
    pass