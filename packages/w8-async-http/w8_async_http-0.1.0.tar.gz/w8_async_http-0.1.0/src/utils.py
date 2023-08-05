# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import iscoroutinefunction
from collections.abc import Callable
from typing import AnyStr


def anystring_to_string(
        string_or_bytes: AnyStr,
        encoding: str = "utf-8"
) -> str:
    """
    str or bytes to str
    :param string_or_bytes:
    :param encoding:
    :return:
    """
    result: str = None
    if isinstance(string_or_bytes, str):
        result = string_or_bytes

    elif isinstance(string_or_bytes, bytes):
        result = string_or_bytes.decode(encoding)

    else:
        raise ValueError(f"value need string or bytes, but got {type(string_or_bytes).__name__}")

    return result


def is_function(value) -> bool:
    """
    check value is Function
    :param value:
    :return:
    """
    return isinstance(value, Callable)


def is_async_function(value) -> bool:
    """
    check value is async function
    :param value:
    :return:
    """
    return all([
        is_function(value),
        iscoroutinefunction(value)
    ])
