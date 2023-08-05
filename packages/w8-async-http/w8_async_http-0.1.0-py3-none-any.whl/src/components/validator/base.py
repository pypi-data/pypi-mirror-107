# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod

from src.components.errors import BaseError


class AbstractValidator(metaclass=ABCMeta):

    def __init__(self, message: str):
        self._message = message

    @property
    def error_message(self):
        return self._message

    def _raise_error(self, error: BaseError):
        if not issubclass(error, BaseError):
            raise ValueError(f"error_klass must be BaseError subclass, but got {type(error).__name__}")
        raise error(self.error_message)

    @abstractmethod
    def validate(self, value, **kwargs) -> bool:
        raise NotImplementedError("NotImplemented .validate(value, **kwargs)")
