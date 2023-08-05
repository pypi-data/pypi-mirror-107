# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from src.core.builder import IRequestBuilder
from src.types_of_py import ResponseType


class IAsyncHttp(object):

    async def request(self, options: IRequestBuilder) -> ResponseType:
        raise NotImplementedError("NotImplemented .request(options) -> ResponseType")

    async def get(self, options: IRequestBuilder) -> ResponseType:
        raise NotImplementedError("NotImplemented .get(options) -> ResponseType")

    async def post(self, options: IRequestBuilder) -> ResponseType:
        raise NotImplementedError("NotImplemented .post(options) -> ResponseType")


class IAsyncHttpManager(object):

    def get_instance(self, *args, **kwargs) -> IAsyncHttp:
        raise NotImplementedError("")

    def add_instance(self, *args, **kwargs) -> None:
        raise NotImplementedError("")

    def delete_instance(self, *args, **kwargs) -> None:
        raise NotImplementedError("")
