# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from httpx import AsyncClient

from src.core.builder import IRequestBuilder
from src.core.client import IAsyncHttp, add_message, remove_message
from src.core.merge import Merged
from src.core.messages import IMessages
from src.types_of_py import HookDict


class LikeAxiosHttp(IAsyncHttp):

    def __init__(self, client: AsyncClient, message: IMessages):
        self._client = client
        self._messages = message
        self._set_default_events(self.messages)

    @property
    def client(self):
        return self._client

    @property
    def messages(self):
        return self._messages

    async def request(self, options: IRequestBuilder):
        self._merge_interceptor(options)
        method, url, optional = self._merge_request(options)
        return await self._request(method, url, **optional)

    async def get(self, options: IRequestBuilder):
        options.method = "get"
        return await self.request(options)

    async def post(self, options: IRequestBuilder):
        options.method = "post"
        return await self.request(options)

    async def close(self):
        if self.messages.empty():
            await self.client.aclose()

    def _merge_request(self, options: IRequestBuilder):
        return Merged.merge_request_from_builder(options)

    def _merge_interceptor(self, options: IRequestBuilder):
        events = self.client.event_hooks
        merged = Merged.merge_hook_from_builder(events, options)
        self._set_events(merged)

    def _set_default_events(self, message: IMessages):
        default = {
            "request": [add_message(message)],
            "response": [remove_message(message)]
        }
        self._set_events(default)

    def _set_events(self, events: HookDict):
        if not isinstance(events, dict):
            return
        self.client.event_hooks = events

    async def _request(self, method: str, url: str, **options):
        return await self.client.request(method, url, **options)

    async def __aenter__(self):
        if self.client.is_closed:
            await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
