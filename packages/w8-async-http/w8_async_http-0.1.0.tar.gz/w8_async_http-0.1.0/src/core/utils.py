# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum


def create_dict_by_enum(klass: Enum) -> dict:
    if not issubclass(klass, Enum):
        raise ValueError(f"klass need a {Enum.__name__} subclass, but got {type(klass).__name__}")
    return {item: item.value for _, item in enumerate(klass)}


def get_from_allowed(key, allowed: dict):
    _allowed = {}
    if isinstance(allowed, dict):
        _allowed.update(allowed)

    if key not in _allowed:
        raise KeyError(f"not found {key} from {_allowed}")

    return _allowed[key]


class AllowedInterceptor(Enum):
    REQUEST = "request"
    RESPONSE = "response"


class AllowedOptional(Enum):
    COOKIES = "cookies"
    DATA = "data"
    HEADERS = "headers"
    JSON = "json"
    PARAMS = "params"


class AllowedUtil(object):
    interceptors = create_dict_by_enum(AllowedInterceptor)
    optional = create_dict_by_enum(AllowedOptional)

    @classmethod
    def allowed_interceptor(cls, name: AllowedInterceptor) -> str:
        """
        allowed interceptor keys
        :param name:
        :return:
        """
        return get_from_allowed(name, cls.interceptors)

    @classmethod
    def allowed_optional(cls, option: AllowedOptional) -> str:
        """
        allowed optional
        :param option:
        :return:
        """
        return get_from_allowed(option, cls.optional)
