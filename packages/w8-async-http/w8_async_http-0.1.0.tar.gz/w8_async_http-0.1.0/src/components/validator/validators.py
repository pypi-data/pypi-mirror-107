# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from src.components.interceptor.base import AsyncInterceptor
from src.components.errors import NotAsyncInterceptorError
from src.components.validator import AbstractValidator
from src.utils import is_async_function


class AsyncInterceptorValidator(AbstractValidator):

    def _is_validated(self, value):
        return any([
            is_async_function(value),
            isinstance(value, AsyncInterceptor)
        ])

    def validate(self, value, **kwargs) -> bool:
        result = self._is_validated(value)
        if not result:
            self._raise_error(NotAsyncInterceptorError)
        return result
