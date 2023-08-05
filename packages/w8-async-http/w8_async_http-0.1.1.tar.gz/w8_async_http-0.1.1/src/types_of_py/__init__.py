# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Any, Callable, Dict, List, Union

from httpx import Request, Response

RequestType = Request
ResponseType = Response
Hook = Callable[[Union[RequestType, ResponseType]], Any]
HookDict = Dict[str, List[Hook]]
