# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
class IMessages(object):
    """
    messages interface
    """

    def empty(self) -> bool:
        raise NotImplementedError()

    def insert(self, message):
        raise NotImplementedError()

    def pop(self, *args, **kwargs):
        raise NotImplementedError()

    def clear(self) -> None:
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()
