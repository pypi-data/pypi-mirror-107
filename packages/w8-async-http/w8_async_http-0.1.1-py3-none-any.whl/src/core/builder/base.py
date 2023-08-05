# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr, Dict, Optional, Union

from src.components.interceptor.manager import AbstractInterceptorManager
from src.components.options import IMethod, IURL, IOptions

AnyStringOrIURL = Union[AnyStr, IURL]
StringOrIMethod = Union[str, IMethod]
OptionalOptions = Optional[IOptions]


class IRequestBuilder(object):

    @property
    def method(self) -> StringOrIMethod:
        raise NotImplementedError("NotImplemented .method -> StringOrIMethod")

    @method.setter
    def method(self, value: StringOrIMethod) -> None:
        raise NotImplementedError("NotImplemented method = value")

    @property
    def url(self) -> AnyStringOrIURL:
        raise NotImplementedError("NotImplemented .url -> AnyStringOrIURL")

    @url.setter
    def url(self, value: AnyStringOrIURL) -> None:
        raise NotImplementedError("NotImplemented .url = value")

    def get_cookies(self) -> OptionalOptions:
        raise NotImplementedError("NotImplemented .get_cookies()")

    def get_data(self) -> OptionalOptions:
        raise NotImplementedError("NotImplemented .get_data()")

    def get_headers(self) -> OptionalOptions:
        raise NotImplementedError("NotImplemented .get_headers()")

    def get_json(self) -> OptionalOptions:
        raise NotImplementedError("NotImplemented .get_json()")

    def get_params(self) -> OptionalOptions:
        raise NotImplementedError("NotImplemented .get_params()")

    def get_interceptors(self) -> Dict[str, AbstractInterceptorManager]:
        raise NotImplementedError("NotImplemented .get_interceptors()")
