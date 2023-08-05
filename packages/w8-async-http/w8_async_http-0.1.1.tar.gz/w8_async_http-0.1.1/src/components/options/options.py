# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import OrderedDict
from typing import Dict


class IOptions(object):

    def set(self, option, value) -> None:
        raise NotImplementedError("NotImplemented .add(option, value) -> None")

    def get(self, option, default=None):
        raise NotImplementedError("NotImplemented .get(option, default) -> None")

    def merge(self, **options) -> None:
        raise NotImplementedError("NotImplemented .merge(**options) -> None")

    def clear(self) -> None:
        raise NotImplementedError("NotImplemented .clear() -> None")

    def to_dict(self) -> Dict:
        raise NotImplementedError("NotImplemented .to_dict() -> Dict")


class Options(IOptions):
    __slots__ = ["_options"]

    def __init__(self):
        self._options = OrderedDict()

    def set(self, option, value) -> None:
        self[option] = value

    def get(self, option, default=None):
        return default if self.empty() else self._options.get(option, default)

    def merge(self, **options) -> None:
        if not options:
            return
        self._options.update(**options)

    def clear(self) -> None:
        if not self.empty():
            self._options.clear()

    def to_dict(self) -> Dict:
        if self.empty():
            return {}
        return {k: v for k, v in self._options.items()}

    def empty(self):
        return not self._options

    def __setitem__(self, key, value):
        self._options[key] = value

    def __getitem__(self, item):
        return self._options[item]

    def __missing__(self, key):
        raise KeyError(f"not found key: {key}")
