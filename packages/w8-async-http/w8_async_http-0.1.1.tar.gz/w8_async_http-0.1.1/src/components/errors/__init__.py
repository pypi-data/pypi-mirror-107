# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
class BaseError(Exception):
    pass


class NotInterceptorError(BaseError):
    pass


class NotAsyncInterceptorError(BaseError):
    pass
