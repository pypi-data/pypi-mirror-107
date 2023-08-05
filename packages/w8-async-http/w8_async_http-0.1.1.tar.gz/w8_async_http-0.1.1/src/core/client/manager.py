# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import defaultdict

from src.core.client import LikeAxiosHttp, IAsyncHttpManager
from src.core.client.factory import AsyncHttpFactory


def _create():
    return AsyncHttpFactory.create()


class AsyncHttpManager(IAsyncHttpManager):
    __shared = defaultdict(_create)
    __slots__ = ["_instances"]

    def __init__(self):
        self._instances = AsyncHttpManager.__shared

    def get_instance(self, name=None) -> LikeAxiosHttp:
        _name = "default"
        if name:
            _name = name
        return self[_name]

    def add_instance(self, key, instance: LikeAxiosHttp) -> None:
        if key in self:
            return
        self[key] = instance

    def delete_instance(self, key: str = None):
        del self[key]

    def __getitem__(self, key):
        if key not in self:
            return self._instances[key]
        return self._instances.get(key)

    def __setitem__(self, key, value):
        if not isinstance(value, LikeAxiosHttp):
            raise ValueError(f"value need LikeAxiosHttp, but got {type(value).__name__}")
        self._instances[key] = value

    def __delitem__(self, key):
        if key not in self:
            del self._instances[key]

    def __contains__(self, key):
        return key in self._instances
