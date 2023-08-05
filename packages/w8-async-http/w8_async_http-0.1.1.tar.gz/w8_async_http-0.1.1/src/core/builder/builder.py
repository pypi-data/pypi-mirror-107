# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import defaultdict
from typing import AnyStr, DefaultDict

from src.components.interceptor import AsyncInterceptorManager, InterceptorOrFunc
from src.components.options import Method, Options, Url
from src.core.builder import AnyStringOrIURL, IRequestBuilder, StringOrIMethod
from src.core.utils import AllowedInterceptor, AllowedOptional, AllowedUtil

DefaultsOptions = DefaultDict[str, Options]
DefaultsManagers = DefaultDict[str, AsyncInterceptorManager]


class RequestBuilder(IRequestBuilder):

    def __init__(self, method: str, url: AnyStr):
        self._method = Method(method)
        self._url = Url(url)
        self._options: DefaultsOptions = defaultdict(Options)
        self._interceptors: DefaultsManagers = defaultdict(AsyncInterceptorManager)

    @property
    def interceptors(self):
        return self._interceptors

    @property
    def options(self):
        return self._options

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value: StringOrIMethod) -> None:
        if isinstance(value, str):
            self._method = Method(value)
        elif isinstance(value, Method):
            self._method = value
        else:
            raise ValueError(f"method need string or Method, but got {type(value).__name__}")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: AnyStringOrIURL) -> None:
        if isinstance(value, (str, bytes)):
            self._url = Url(value)
        elif isinstance(value, Url):
            self._url = value
        else:
            raise ValueError(f"url need string or Url, but got {type(value).__name__}")

    def add_cookies(self, key: str, value: AnyStr):
        """
        add cookies, key, value
        :param key:
        :param value:
        :return:
        """
        return self._add_to_options(
            AllowedOptional.COOKIES, key, value
        )

    def get_cookies(self):
        return self._get_from_options(AllowedOptional.COOKIES)

    def add_data(self, key: str, value):
        """
        add data, key, value
        :param key:
        :param value:
        :return:
        """
        return self._add_to_options(
            AllowedOptional.DATA, key, value
        )

    def get_data(self):
        return self._get_from_options(AllowedOptional.DATA)

    def add_headers(self, key: str, value: AnyStr):
        """
        add headers, key, value
        :param key:
        :param value:
        :return:
        """
        return self._add_to_options(
            AllowedOptional.HEADERS, key, value
        )

    def get_headers(self):
        return self._get_from_options(AllowedOptional.HEADERS)

    def add_json(self, key: str, value):
        """
        add json, key, value
        :param key:
        :param value:
        :return:
        """
        return self._add_to_options(
            AllowedOptional.JSON, key, value
        )

    def get_json(self):
        return self._get_from_options(AllowedOptional.JSON)

    def add_params(self, key: str, value):
        """
        add params, key, value
        :param key:
        :param value:
        :return:
        """
        return self._add_to_options(
            AllowedOptional.PARAMS, key, value
        )

    def get_params(self):
        return self._get_from_options(AllowedOptional.PARAMS)

    def add_request_interceptor(self, interceptor_or_func: InterceptorOrFunc):
        """
        add request interceptor
        :param interceptor_or_func:
        :return:
        """
        return self._add_to_interceptors(
            AllowedInterceptor.REQUEST, interceptor_or_func
        )

    def add_response_interceptor(self, interceptor_or_func: InterceptorOrFunc):
        """
        add response interceptor
        :param interceptor_or_func:
        :return:
        """
        return self._add_to_interceptors(
            AllowedInterceptor.RESPONSE, interceptor_or_func
        )

    def get_interceptors(self):
        return dict(self._get_from_interceptors(allowed) for _, allowed in enumerate(AllowedInterceptor))

    def _add_to_options(self, option: AllowedOptional, key, value) -> None:
        """
        add optional
        :param option:
        :param key:
        :param value:
        :return:
        """
        options = self._get_optional_from_options(
            AllowedUtil.allowed_optional(option)
        )
        options.set(key, value)

    def _get_from_options(self, option: AllowedOptional):
        """
        get optional
        :param option:
        :return:
        """
        return self.options.get(AllowedUtil.allowed_optional(option))

    def _get_optional_from_options(self, key: str) -> Options:
        """
        get option from options
        :param key:
        :return:
        """
        return self._get_from_defaults(self.options, key)

    def _add_to_interceptors(self,
                             name: AllowedInterceptor,
                             interceptor_or_func: InterceptorOrFunc):
        """
        添加拦截器
        :param name:
        :param interceptor_or_func:
        :return:
        """
        manager = self._get_manager_from_interceptors(AllowedUtil.allowed_interceptor(name))
        return manager.add(interceptor_or_func)

    def _get_from_interceptors(self, name: AllowedInterceptor):
        """
        获取拦截器
        :param name:
        :return:
        """
        key = AllowedUtil.allowed_interceptor(name)
        return key, self._get_manager_from_interceptors(key)

    def _get_manager_from_interceptors(self, key: str) -> AsyncInterceptorManager:
        """
        get manager form interceptors
        :param key:
        :return:
        """
        return self._get_from_defaults(self.interceptors, key)

    def _get_from_defaults(self, defaults: DefaultDict, key):
        if not isinstance(defaults, defaultdict):
            raise ValueError(f"defaults need defaultdict, but got {type(defaults).__name__}")
        return defaults[key]
