# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from configparser import ConfigParser
from enum import Enum

from src.core.conf import IReader
from src.core.utils import create_dict_by_enum, get_from_allowed


class ConfigOptions(Enum):
    BASE_URL = "BASE_URL"
    MAX_CONNECTION = "MAX_CONNECTION"
    MAX_KEEPALIVE = "MAX_KEEPALIVE"
    TIMEOUT = "TIMEOUT"


class ConfigReader(IReader):
    options = create_dict_by_enum(ConfigOptions)

    def __init__(self, parser: ConfigParser):
        self._parser = parser
        self._current = "DEFAULT"

    @property
    def parser(self):
        return self._parser

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, section: str) -> None:
        if not self.has_section(section):
            return
        self._current = section

    def has_section(self, section):
        return self.parser.has_section(section)

    def read_base_url(self) -> str:
        return self.read_from_section(
            self.current,
            ConfigOptions.BASE_URL
        ).strip("'").strip('"')

    def read_max_connection(self) -> int:
        return self.read_int_from_section(
            self.current,
            ConfigOptions.MAX_CONNECTION
        )

    def read_max_keepalive(self) -> int:
        return self.read_int_from_section(
            self.current,
            ConfigOptions.MAX_KEEPALIVE
        )

    def read_timeout(self) -> float:
        return float(self.read_int_from_section(
            self.current,
            ConfigOptions.TIMEOUT
        ))

    def read_from_section(self, section: str, option: ConfigOptions):
        return self._parser.get(
            self._get_section(section),
            self._allowed_option(option)
        )

    def read_int_from_section(self, section: str, option: ConfigOptions):
        return self.parser.getint(
            self._get_section(section),
            self._allowed_option(option)
        )

    def _get_section(self, section: str) -> str:
        result: str = section
        if not self.has_section(result):
            result = self.current
        return result

    def _allowed_option(self, option: ConfigOptions):
        return get_from_allowed(option, ConfigReader.options)
