# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from src.components.options import IOptions
from src.core.builder import IRequestBuilder
from src.core.merge import IMerged, Merged3Tup, MergedDictHookList


class Merged(IMerged):

    @classmethod
    def merge_request_from_builder(cls, builder: IRequestBuilder) -> Merged3Tup:
        """
        合并 request
        :param builder:
        :return:
        """
        method = cls._merged_method(builder)
        url = cls._merged_url(builder)
        options = cls._merged_options(builder)
        return method, url, options

    @classmethod
    def merge_hook_from_builder(cls,
                                hook: MergedDictHookList,
                                builder: IRequestBuilder):
        """
        合并 hook
        :param hook:
        :param builder:
        :return:
        """
        result: MergedDictHookList = {}
        interceptors = builder.get_interceptors()
        for k in interceptors:
            if k in hook:
                hook[k].extend(interceptors[k])
                result[k] = hook[k]
        return result

    @classmethod
    def _merged_method(cls, builder: IRequestBuilder):
        return str(builder.method)

    @classmethod
    def _merged_url(cls, builder: IRequestBuilder):
        return str(builder.url)

    @classmethod
    def _merged_options(cls, builder: IRequestBuilder):
        return {
            "cookies": cls._merged_cookies(builder),
            "data": cls._merged_data(builder),
            "headers": cls._merged_headers(builder),
            "json": cls._merged_json(builder),
            "params": cls._merged_params(builder)
        }

    @classmethod
    def _merged_cookies(cls, builder: IRequestBuilder):
        return cls._option_to_dict(builder.get_cookies())

    @classmethod
    def _merged_data(cls, builder: IRequestBuilder):
        return cls._option_to_dict(builder.get_data())

    @classmethod
    def _merged_headers(cls, builder: IRequestBuilder):
        return cls._option_to_dict(builder.get_headers())

    @classmethod
    def _merged_json(cls, builder: IRequestBuilder):
        return cls._option_to_dict(builder.get_json())

    @classmethod
    def _merged_params(cls, builder: IRequestBuilder):
        return cls._merged_data(builder.get_params())

    @classmethod
    def _option_to_dict(cls, options: IOptions):
        return options.to_dict() if options else None
