# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from configparser import ConfigParser
from enum import Enum

from common.src import get_from_allowed
from common.src import EnumUtil
from common.src import is_string


class ConfigOptions(Enum):
    pass


class BaseReader(object):
    """
    配置读取器
    """
    DEFAULT = "DEFAULT"

    def __init__(self,
                 parser: ConfigParser,
                 options_klass: ConfigOptions):
        self._check_parser(parser)
        self._parser = parser
        self._options = EnumUtil.create_dict_by_enum(options_klass)
        self._default = BaseReader.DEFAULT

    @property
    def options(self) -> dict:
        return self._options

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, parser: ConfigParser) -> None:
        self._check_parser(parser)
        self._parser = parser

    def read_float(self, section: str, option: ConfigOptions):
        return self._parser.getfloat(
            self._get_section(section),
            self._get_allowed_option(option)
        )

    def read_int(self, section: str, option: ConfigOptions):
        return self._parser.getint(
            self._get_section(section),
            self._get_allowed_option(option)
        )

    def read_string(self, section: str, option: ConfigOptions):
        return self._strip_quota(
            self._parser.get(
                self._get_section(section),
                self._get_allowed_option(option)
            )
        )

    def set_default(self, section: str) -> None:
        if not self._is_section(section):
            raise ValueError(f"section name need string, but got {type(section).__name__}")
        self._default = section.upper()

    def has(self, section: str) -> bool:
        if not self._is_section(section):
            return False
        return self._parser.has_section(section)

    def _get_allowed_option(self, option: ConfigOptions):
        """
        allowed option
        :param option:
        :return:
        """
        return get_from_allowed(option, self._options)

    def _get_section(self, section: str):
        return BaseReader.DEFAULT if not self.has(section) else section

    def _strip_quota(self, result: str) -> str:
        if not is_string(result):
            raise ValueError(f"result need string, but got {type(result).__name__}")
        if not result:
            return result
        return result.strip("'").strip('"')

    def _is_section(self, section):
        return isinstance(section, str)

    def _check_parser(self, parser: ConfigParser):
        if not isinstance(parser, ConfigParser):
            raise ValueError(f"parser need a ConfigParser, but got {type(parser).__name__}")


class BaseGenerator(object):
    """
    配置生成器
    """

    def __init__(self, reader: BaseReader):
        self._reader = reader

    @property
    def reader(self) -> BaseReader:
        return self._reader

    @reader.setter
    def reader(self, value: BaseReader) -> None:
        if not self._is_reader(value):
            return
        self._reader = value

    def _is_reader(self, value):
        return isinstance(value, BaseReader)
