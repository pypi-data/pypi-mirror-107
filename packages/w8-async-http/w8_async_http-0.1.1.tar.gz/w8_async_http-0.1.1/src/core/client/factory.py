# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Union

from httpx import AsyncClient, Limits, Timeout, URL

from src.core.conf import IGenerator, Config
from src.core.client import LikeAxiosHttp
from src.core.messages import MessageQueue


class IAsyncHttpFactory(object):

    @classmethod
    def create(cls, *args, **kwargs) -> LikeAxiosHttp:
        raise NotImplementedError("NotImplemented .create() -> LikeAxiosHttp")


class AsyncHttpFactory(IAsyncHttpFactory):
    _default_config = Config.generate_from_ini("config.ini")

    @classmethod
    def create(cls):
        client = cls.create_client_from_config(cls._default_config)
        messages = MessageQueue()
        return LikeAxiosHttp(client, messages)

    @classmethod
    def create_client_from_config(cls, config: IGenerator) -> AsyncClient:
        return AsyncClient(
            base_url=cls._create_base_url(config),
            limits=cls._create_limits(config),
            timeout=cls._create_timeout(config)
        )

    @classmethod
    def set_config(cls, config_or_filename: Union[str, IGenerator]):
        _config: IGenerator = None
        if isinstance(config_or_filename, IGenerator):
            _config = config_or_filename
        elif isinstance(config_or_filename, str):
            _config = Config.generate_from_ini(_config)
        else:
            raise ValueError(f"config need filename or IGenerator, but got {type(config_or_filename).__name__}")
        cls._default_config = _config

    @classmethod
    def _create_base_url(cls, config: IGenerator):
        return URL(config.base_url)

    @classmethod
    def _create_limits(cls, config: IGenerator):
        return Limits(
            max_connections=config.max_connection,
            max_keepalive_connections=config.max_keepalive
        )

    @classmethod
    def _create_timeout(cls, config: IGenerator):
        return Timeout(
            config.timeout
        )
