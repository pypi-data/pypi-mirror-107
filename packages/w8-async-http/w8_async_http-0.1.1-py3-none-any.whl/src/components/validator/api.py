# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from src.components.validator import AbstractValidator, AsyncInterceptorValidator
from src.components.validator.factory import ValidatorFactory


def is_validate(klass: AbstractValidator, message: str, value) -> bool:
    validator = ValidatorFactory.create(klass, message)
    return validator.validate(value)


def is_async_interceptor(value):
    return is_validate(
        AsyncInterceptorValidator,
        f"value need a async function or AsyncInterceptor, but got {type(value).__name__}",
        value
    )
