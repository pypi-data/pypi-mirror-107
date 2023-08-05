# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
class IMethod(object):

    def __str__(self) -> str:
        raise NotImplementedError("NotImplemented .__str__() -> str")


class Method(IMethod):

    def __init__(self, value: str):
        self._value = value
        self._methods = {
            "delete": "DELETE",
            "get": "GET",
            "post": "POST",
            "put": "PUT"
        }

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, method: str):
        if method in self._methods:
            self._value = method

    def add_method(self, key: str, value: str):
        if any([not isinstance(key, str), not isinstance(value, str)]):
            raise ValueError("key or value need string")

        if key in self._methods:
            return

        self._methods[key.lower()] = value.upper()

    def __str__(self):
        _method = self.value
        if _method not in self._methods:
            _method = "get"
        return self._methods[_method]
