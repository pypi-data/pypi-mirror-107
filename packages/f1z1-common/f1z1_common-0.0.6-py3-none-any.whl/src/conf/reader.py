# @Time     : 2021/5/28
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
try:
    import simplejson as json
except ImportError:
    import json
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from configparser import ConfigParser
from enum import Enum
from typing import Dict, DefaultDict

from common.src.utils import (
    ExtensionNameList,
    EnumUtil,
    Encoding,
    get_from_allowed,
    PathUtil,
    PathTypes,
    StringsUtil
)
from common.src.validator.is_validators import (
    is_any_string,
    is_dict,
    is_string,
    is_int,
    is_float,
    is_number
)


class AllowedOptions(Enum):
    pass


class AbstractConfigReader(metaclass=ABCMeta):
    """
    config reader abc class
    """

    def __init__(self,
                 filename: PathTypes, *,
                 options: AllowedOptions,
                 extension_names: ExtensionNameList = None):
        self._file = filename
        self._options = self._to_options(options)
        self._extension_names = [] if not extension_names else extension_names

    @property
    def file(self):
        return self._file

    @property
    def extension_names(self) -> ExtensionNameList:
        return self._extension_names

    @abstractmethod
    def get_int(self, node: str, option) -> int:
        raise NotImplementedError("NotImplemented .get_int(node, option) -> int")

    @abstractmethod
    def get_float(self, node: str, option) -> float:
        raise NotImplementedError("NotImplemented .get_float(node, option) -> float")

    @abstractmethod
    def get_string(self, node: str, option) -> str:
        raise NotImplementedError("NotImplemented .get_string(node, option) -> str")

    def _to_int(self, value):
        if is_int(value):
            return value
        elif is_number(value):
            return int(value)
        else:
            raise ValueError(f"value need float or int, but got {type(value).__name__}")

    def _to_float(self, value):
        if is_float(value):
            return value
        elif is_number(value):
            return float(value)
        else:
            raise ValueError(f"value need float or int, but got {type(value).__name__}")

    def _to_string(self, value):
        if is_string(value):
            return value
        elif is_any_string(value):
            return StringsUtil.anystr_to_string(value)
        return str(value)

    def _get_allowed_option(self, option: AllowedOptions) -> str:
        result = get_from_allowed(option, self._options)
        if not is_string(result):
            raise ValueError(f"option need string, but got {type(result).__name__}")
        return result

    def _to_options(self, options: AllowedOptions) -> dict:
        return EnumUtil.create_dict_by_enum(options)

    def is_config_file(self, file: PathTypes) -> bool:
        return PathUtil.is_endswith_ext(file, self.extension_names)


class IniReader(AbstractConfigReader):
    DEFAULT = "DEFAULT"

    def __init__(self,
                 filename: PathTypes,
                 *,
                 options: AllowedOptions,
                 extension_names: ExtensionNameList = None):
        super().__init__(
            filename,
            options=options,
            extension_names=["ini"]
        )
        self._parser = self._init_parser(self.file)

    def get_float(self, node: str, option: AllowedOptions) -> float:
        return self._parser.getfloat(
            section=self._get_node(node),
            option=self._get_allowed_option(option)
        )

    def get_int(self, node: str, option: AllowedOptions) -> int:
        return self._parser.getint(
            section=self._get_node(node),
            option=self._get_allowed_option(option)
        )

    def get_string(self, node: str, option: AllowedOptions) -> str:
        result = self._parser.get(
            section=self._get_node(node),
            option=self._get_allowed_option(option)
        )
        return self._strip_quota(result)

    def has_node(self, node):
        if node is None:
            return False
        return self._parser.has_section(node)

    def _strip_quota(self, result: str) -> str:
        if not is_string(result):
            raise ValueError(f"result need string, but got {type(result).__name__}")
        if not result:
            return result
        return result.strip("'").strip('"')

    def _get_node(self, node: str):
        return IniReader.DEFAULT if not self.has_node(node) else node

    def _init_parser(self, file: PathTypes) -> ConfigParser:
        parser = ConfigParser()
        self._read_ini(parser, file)
        return parser

    def _read_ini(self, parser: ConfigParser, file: PathTypes):
        if self.is_config_file(file):
            parser.read(file)


class JsonReader(AbstractConfigReader):
    class JsonNode(object):

        def __init__(self, **kwargs):
            self._node = {} if not kwargs else kwargs

        def get(self, item, default=None):
            return self._node.get(item, default)

    def __init__(self,
                 filename: PathTypes,
                 *,
                 options: AllowedOptions,
                 extension_names: ExtensionNameList = None,
                 encoding: Encoding = Encoding.UTF_8):
        super().__init__(
            filename, options=options, extension_names=["json"]
        )
        self._parser = self._init_parser(self.file, encoding)

    def get_float(self, node: str, option: AllowedOptions) -> float:
        return self._get_from_parser(node, option, self._to_float)

    def get_int(self, node: str, option: AllowedOptions) -> int:
        return self._get_from_parser(node, option, self._to_int)

    def get_string(self, node: str, option: AllowedOptions) -> str:
        return self._get_from_parser(node, option, self._to_string)

    def _get_from_parser(self, node, option: AllowedOptions, callback):
        json_node = self._get_node(node)
        allowed = self._get_allowed_option(option)
        result = json_node.get(allowed)
        if result is None:
            raise KeyError(f"not found {allowed} from {node}")
        return callback(result)

    def _get_node(self, node):
        return self._parser[node]

    def _init_parser(self,
                     file: PathTypes,
                     encoding: Encoding = Encoding.UTF_8) -> DefaultDict[str, JsonNode]:
        data = self._read_json(file, encoding)
        filtered = self._filter_json(data)
        return defaultdict(JsonReader.JsonNode, filtered)

    def _filter_json(self, result: dict) -> Dict[str, JsonNode]:
        if not is_dict(result):
            return {}
        return {k: JsonReader(**v) for k, v in result.items() if is_dict(v)}

    def _read_json(self, file, encoding: Encoding) -> dict:
        result = {}
        if self.is_config_file(file):
            with open(file, mode="r") as jf:
                result = json.load(jf, encoding=StringsUtil.to_encoding(encoding))
        return result
