# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr
from urllib.parse import urlparse

from src.utils import anystring_to_string


class IURL(object):

    def __str__(self) -> str:
        raise NotImplementedError("NotImplemented .__str__() -> str")


class Url(IURL):
    TRANSFERS = {
        "http": "http://",
        "https": "https://",
        "ftp": "ftp://",
        "ws": "ws://",
        "wss": "wss://"
    }

    def __init__(self, value: AnyStr):
        self._value = self._parser(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, url: AnyStr) -> None:
        self._value = self._parser(url)

    @property
    def scheme(self):
        return self._value.scheme

    @property
    def params(self):
        return self._value.params

    @property
    def query(self):
        return self._value.query

    def _parser(self, value: AnyStr):
        result = urlparse(anystring_to_string(value))
        scheme = result.scheme
        transfers = Url.TRANSFERS
        if scheme not in transfers:
            raise ValueError(f"transfer scheme need {', '.join(transfers)}")
        return result

    def __str__(self):
        return anystring_to_string(self.value.geturl())
