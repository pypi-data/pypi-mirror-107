# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
"""
interceptor manager file
"""
from abc import ABCMeta, abstractmethod
from typing import Callable, List, Union

from src.components.interceptor import AsyncInterceptor
from src.components.validator import is_async_interceptor

InterceptorOrFunc = Union[Callable, AsyncInterceptor]


class AbstractInterceptorManager(metaclass=ABCMeta):

    def __init__(self):
        self._interceptors: List[InterceptorOrFunc] = []

    @abstractmethod
    def add(self, interceptor_or_func: InterceptorOrFunc) -> int:
        raise NotImplementedError("NotImplemented .add(interceptor) -> int")

    @property
    def interceptors(self):
        return self._interceptors

    @property
    def length(self) -> int:
        return len(self.interceptors)

    def clear(self):
        if not self.empty():
            self.interceptors.clear()

    def empty(self):
        return not self.length

    def remove(self, interceptor_or_func: InterceptorOrFunc) -> int:
        if self.empty():
            return self.length

        idx = self._find(interceptor_or_func)
        if idx > -1:
            self.interceptors.pop(interceptor_or_func)

        return self.length

    def __iter__(self):
        if not self.empty():
            for _, item in enumerate(self.interceptors):
                yield item

    def __add__(self, other):
        if isinstance(other, AbstractInterceptorManager):
            self.interceptors.extend(other.interceptors)
        return self

    def _is_exists(self, interceptor: InterceptorOrFunc) -> bool:
        return interceptor in self.interceptors

    def _find(self, interceptor) -> int:
        return -1 if not self._is_exists(interceptor) else self.interceptors.index(interceptor)


class AsyncInterceptorManager(AbstractInterceptorManager):

    def add(self, interceptor_or_func: AsyncInterceptor) -> int:
        _interceptor = self._validated_interceptor(interceptor_or_func)
        idx = self._find(_interceptor)
        if idx < 0:
            self.interceptors.append(_interceptor)
        return self.length

    def _validated_interceptor(self, value) -> AsyncInterceptor:
        result = value
        is_async_interceptor(result)
        return result
