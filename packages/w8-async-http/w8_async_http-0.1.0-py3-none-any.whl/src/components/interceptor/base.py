# @Time     : 2021/5/24
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
"""
interceptor interface file
"""


class AsyncInterceptor(object):
    """
    async interceptor interface
    """

    async def __call__(self, value, **kwargs):
        raise NotImplementedError("NotImplemented .__call__(value, **kwargs)")
