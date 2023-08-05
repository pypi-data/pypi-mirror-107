# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from configparser import ConfigParser

from src.core.conf import IConfig
from src.core.conf.generator import ConfigGenerator
from src.core.conf.reader import ConfigReader
from src.path import PathUtil


class Config(IConfig):

    @classmethod
    def generate_from_ini(cls, filename: str, **kwargs) -> ConfigGenerator:
        ini_file = cls._get_ini(filename)
        parser = cls._create_parser(ini_file)
        reader = ConfigReader(parser)
        return ConfigGenerator(reader)

    @classmethod
    def _create_parser(cls, file):
        parser = ConfigParser()
        parser.read(file)
        return parser

    @classmethod
    def _get_ini(cls, filename: str):
        _filename = "config.ini"
        if all([filename, isinstance(filename, str)]):
            _filename = filename
        return PathUtil.get_resolve_ini(filename)
