# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from src.core.builder import IRequestBuilder
from src import AsyncHttpManager


class AsyncHttpUtils(object):
    _manager = AsyncHttpManager()

    @classmethod
    async def request(cls, options: IRequestBuilder):
        async with cls._manager.get_instance() as client:
            return await client.request(options)

    @classmethod
    async def post(cls, options: IRequestBuilder):
        options.method = "post"
        return await cls.request(options)

    @classmethod
    async def get(cls, options: IRequestBuilder):
        options.method = "get"
        return await cls.request(options)
