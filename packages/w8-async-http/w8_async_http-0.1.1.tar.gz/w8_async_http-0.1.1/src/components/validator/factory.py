# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from functools import partial

from src.components.validator.base import AbstractValidator


class IValidatorFactory(object):

    @classmethod
    def create(cls, *args, **kwargs) -> AbstractValidator:
        raise NotImplementedError("NotImplemented .create() -> AbstractValidator")


class ValidatorFactory(IValidatorFactory):

    @classmethod
    def create(cls, klass: AbstractValidator, message: str, **kwargs) -> AbstractValidator:
        f = cls._factory(klass)
        return f(message, **kwargs)

    @classmethod
    def _factory(cls, klass: AbstractValidator):
        return partial(cls._validated_klass(klass))

    @classmethod
    def _validated_klass(cls, klass) -> AbstractValidator:
        _klass: AbstractValidator = klass
        if not issubclass(_klass, AbstractValidator):
            raise ValueError(f"klass need a {AbstractValidator.__name__} subclass, but got {type(klass).__name__}")
        return _klass


def is_validate(klass: AbstractValidator, message: str, value) -> bool:
    validator = ValidatorFactory.create(klass, message)
    return validator.validate(value)
