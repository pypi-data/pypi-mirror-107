from collections.abc import Iterable, Mapping, MutableMapping
from functools import reduce, singledispatch
from operator import getitem

__version__ = "0.0.0"
__version_info__ = tuple(__version__.split("."))


class DeepDict(MutableMapping):
    def __init__(self, _obj=None, **kwargs):

        self._items = dict()
        if _obj is None:
            pass
        elif isinstance(_obj, Mapping):
            for key, value in _obj.items():
                self[key] = value
        elif isinstance(_obj, Iterable):
            for key, value in _obj:
                self[key] = value
        else:
            raise TypeError(f"{type(_obj).__name__!r} is not iterable")
        self._items.update(kwargs)

        # Replace all standard dictionaries near the root with DeepDict
        keys = [key for key, value in self._items.items() if isinstance(value, dict)]
        for key in keys:
            self._items[key] = type(self)(self._items[key])

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, k):
        if isinstance(k, tuple):
            self._validate_key(k)
            return reduce(getitem, k, self)
        return self._items[k]

    def __setitem__(self, k, v):
        if isinstance(k, tuple):
            self._validate_key(k)
            d = self
            for key in k[:-1]:
                if key not in d:
                    d[key] = type(self)()
                d = d[key]
                if not isinstance(d, MutableMapping):
                    raise TypeError(f"{key} does not refer to a MutableMapping")
            d[k[-1]] = v
        else:
            self._items[k] = type(self)(v) if isinstance(v, dict) else v

    def _validate_key(self, k):
        if len(k) == 0:
            raise KeyError(f"{type(self).__name__} key {k!r} does not have at least one component")

    def __delitem__(self, k):
        if isinstance(k, tuple):
            self._validate_key(k)
            config = self
            for key in k[:-1]:
                config = config[key]
                if not isinstance(config, MutableMapping):
                    raise TypeError(f"{key} does not refer to a MutableMapping")
            del config[k[-1]]
        else:
            del self._items[k]

    def __repr__(self):
        return f"{type(self).__name__}({self._items!r})"

    def to_dict(self):
        return {key: value.to_dict() if isinstance(value, DeepDict) else value for key, value in self._items.items()}


class DottedDeepDict(DeepDict):
    def __getitem__(self, k):
        return super().__getitem__(self._split_key(k))

    def __setitem__(self, k, v):
        return super().__setitem__(self._split_key(k), v)

    def __delitem__(self, k):
        return super().__delitem__(self._split_key(k))

    @staticmethod
    def _split_key(k):
        # TODO: Handle quoted sections in keys a la TOML
        if isinstance(k, str) and "." in k:
            k = tuple(k.split("."))
        return k


@singledispatch
def to_dict(d):
    """Convert a DeepDict to a regular dictionary."""
    raise NotImplementedError(f"No implementation of to_dict for {type(d).__name__}")


@to_dict.register(dict)
def _(d: dict):
    return d


@to_dict.register(DeepDict)
def _(d: DeepDict):
    return d.to_dict()


if __name__ == "__main__":
    d = DottedDeepDict([("gjenta.environment.command", 42)])
    print(d["gjenta.environment.command"])
    print(d["gjenta"]["environment.command"])
    print(d["gjenta", "environment", "command"])
    print(d.to_dict())

    e = DottedDeepDict(
        {
            "hello": {
                "fr": "bonjour",
                "en": "hello",
                "no": "hei",
            },
            "goodbye": {"fr": "au revoir", "en": "goodbye", "no": "ha det", "ba": {"a": 5, "b": 6}},
        }
    )
    print(e)
    print(e.to_dict())
