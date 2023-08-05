# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
class IReader(object):

    def read_max_connection(self) -> int:
        raise NotImplementedError()

    def read_max_keepalive(self) -> int:
        raise NotImplementedError()

    def read_timeout(self) -> float:
        raise NotImplementedError()

    def read_base_url(self) -> str:
        raise NotImplementedError()


class IGenerator(object):

    @property
    def base_url(self) -> str:
        raise NotImplementedError("")

    @property
    def max_connection(self) -> int:
        raise NotImplementedError("")

    @property
    def max_keepalive(self) -> int:
        raise NotImplementedError("")

    @property
    def timeout(self) -> float:
        raise NotImplementedError("")


class IConfig(object):

    @classmethod
    def generate_from_ini(cls, filename: str, **kwargs) -> IGenerator:
        raise NotImplementedError("")
