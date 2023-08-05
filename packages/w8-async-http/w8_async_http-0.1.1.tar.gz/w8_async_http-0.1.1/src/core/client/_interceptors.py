# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from functools import partial

from src.components.interceptor import AsyncInterceptor
from src.core.messages import IMessages
from src.types_of_py import RequestType, ResponseType


class AsyncInsertMessage(AsyncInterceptor):

    def __init__(self, messages: IMessages):
        self._messages = messages

    async def __call__(self, request: RequestType, **kwargs):
        self._messages.insert(request)


class AsyncRemoveMessage(AsyncInterceptor):

    def __init__(self, messages: IMessages):
        self._messages = messages

    async def __call__(self, response: ResponseType, **kwargs):
        if not self._messages.empty():
            self._messages.pop()


def _validated_klass(klass: AsyncInterceptor) -> AsyncInterceptor:
    _klass = klass
    if not issubclass(_klass, AsyncInterceptor):
        raise ValueError(f"klass need a {AsyncInterceptor.__name__}, but got {type(klass).__name__}")
    return _klass


def _factory(klass: AsyncInterceptor):
    return partial(_validated_klass(klass))


def creator(klass: AsyncInterceptor, message: IMessages):
    f = _factory(klass)
    return f(message)


def add_message(message: IMessages) -> AsyncInsertMessage:
    return creator(AsyncInsertMessage, message)


def remove_message(message: IMessages) -> AsyncRemoveMessage:
    return creator(AsyncRemoveMessage, message)
