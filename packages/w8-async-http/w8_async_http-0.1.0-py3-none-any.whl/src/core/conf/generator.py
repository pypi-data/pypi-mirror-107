# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from src.core.conf import IReader, IGenerator


class ConfigGenerator(IGenerator):

    def __init__(self, reader: IReader):
        self._base_url = reader.read_base_url()
        self._max_connection = reader.read_max_connection()
        self._max_keepalive = reader.read_max_keepalive()
        self._timeout = reader.read_timeout()

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def max_connection(self) -> int:
        return self._max_connection

    @property
    def max_keepalive(self) -> int:
        return self._max_keepalive

    @property
    def timeout(self) -> int:
        return self._timeout
