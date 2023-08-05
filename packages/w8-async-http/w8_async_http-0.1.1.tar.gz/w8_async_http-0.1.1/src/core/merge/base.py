# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Callable, Dict, List, Tuple
from src.core.builder import IRequestBuilder

MergedDictHookList = Dict[str, List[Callable]]
Merged3Tup = Tuple[str, str, Dict]


class IMerged(object):

    @classmethod
    def merge_request_from_builder(cls, builder: IRequestBuilder) -> Merged3Tup:
        raise NotImplementedError("")

    @classmethod
    def merge_hook_from_builder(cls, hook: MergedDictHookList, builder: IRequestBuilder):
        raise NotImplementedError("")
