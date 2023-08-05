# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import deque
from src.core.messages import IMessages


class MessageQueue(IMessages):

    def __init__(self, max_len: int = None):
        max_len = 2 ** 31 if not isinstance(max_len, int) else max_len
        self._messages = deque(maxlen=max_len)

    @property
    def length(self) -> int:
        return len(self._messages)

    @property
    def messages(self):
        return self._messages

    def empty(self):
        return not self.length

    def insert(self, message):
        self.messages.append(message)
        return self.length

    def pop(self):
        if self.empty():
            return None
        return self.messages.popleft()

    def clear(self):
        self.messages.clear()

    def __iter__(self):
        while True:
            if self.empty():
                break
            yield self.pop()
