# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from pathlib import Path

BASE_PATH = Path(__file__).parent


class PathUtil(object):

    @staticmethod
    def is_file_by_ext(path: Path, ext: str) -> bool:
        return path.suffix.endswith(ext)

    @classmethod
    def get_resolve_from_src(cls, *paths) -> Path:
        return BASE_PATH.resolve().joinpath(*paths)

    @classmethod
    def get_resolve_ini(cls, filename: str) -> Path:
        path = cls.get_resolve_from_src(filename)
        if not cls.is_file_by_ext(path, "ini"):
            raise ValueError(f"Not Found file from {path}")
        return path
