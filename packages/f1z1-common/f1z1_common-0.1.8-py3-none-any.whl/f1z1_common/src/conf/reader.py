# @Time     : 2021/5/28
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
try:
    import simplejson as json
except ImportError:
    import json
from collections import defaultdict
from configparser import ConfigParser
from typing import Dict, DefaultDict, List, Union
from uuid import uuid4

from .base import AbstractConfReader
from ..utils import (
    ExtensionNameList,
    Encoding,
    PathTypes
)
from ..validator.is_validators import (
    is_dict,
    is_none,
    is_list,
    is_string
)


class IniReader(AbstractConfReader):
    DEFAULT = "DEFAULT"
    __file_ext__ = ".ini"

    def __init__(self,
                 file: PathTypes,
                 ext_names: ExtensionNameList = None,
                 encoding: Encoding = None):
        super().__init__(file, ext_names, encoding)

        if ".ini" not in self._ext_names:
            self._ext_names.append(IniReader.__file_ext__)

        self._parser = self._init_parser(self.file)

    def get_float(self, node: str, option: str) -> float:
        node = self._get_node_from_section(node)
        result = self._parser.getfloat(node, self._get_option_from_section(node, option))
        return result

    def get_int(self, node: str, option: str) -> int:
        node = self._get_node_from_section(node)
        result = self._parser.getint(node, self._get_option_from_section(node, option))
        return result

    def get_string(self, node: str, option: str) -> str:
        node = self._get_node_from_section(node)
        result = self._parser.get(node, self._get_option_from_section(node, option))
        return self._strip_quota(result)

    def has_node(self, node: str):
        if is_none(node):
            return False
        return self._parser.has_section(node)

    def _get_option_from_section(self, node: str, option: str):
        result = option
        if not self._parser.has_option(node, result):
            raise ValueError("not found option {option}")
        return result

    def _get_node_from_section(self, node: str):
        return IniReader.DEFAULT if not self.has_node(node) else node

    def _strip_quota(self, result: str) -> str:
        if not is_string(result):
            raise ValueError(f"result need string, but got {type(result).__name__}")
        if not result:
            return result
        return result.strip("'").strip('"')

    def _init_parser(self, file: PathTypes) -> ConfigParser:
        parser = ConfigParser()
        self._read_ini(parser, file)
        return parser

    def _read_ini(self, parser: ConfigParser, file: PathTypes):
        if self.is_config_file(file):
            parser.read(file, encoding=self._to_encoding(self._encoding))


Number = Union[float, int]
JsonTypes = Union[bool, Number, Dict, List, None]


class JsonNode(object):

    def __init__(self, key: str, data: JsonTypes = None):
        self._key = key
        self._data = self._create_by_json(key, data)

    def get(self, option: str, default=None):
        return self._data.get(option, default)

    def has_option(self, option):
        return option in self._data

    def _create_by_json(self, key: str, data: JsonTypes) -> dict:
        if is_dict(data):
            return self._by_dict(key, data)
        elif is_list(data):
            return self._by_list(key, data)
        else:
            return self._by_value(key, data)

    def _by_dict(self, key, data: Dict):
        return {k: v for k, v in data.items()}

    def _by_list(self, key, data: List):
        return {index: value for index, value in enumerate(data)}

    def _by_value(self, key, data: Union[bool, None, Number]):
        return {key: data}


class JsonReader(AbstractConfReader):
    __file_ext__ = ".json"

    def __init__(self,
                 file: PathTypes,
                 ext_names: ExtensionNameList = None,
                 encoding: Encoding = None):
        super().__init__(file, ext_names, encoding)

        if ".json" not in self._ext_names:
            self._ext_names.append(JsonReader.__file_ext__)

        self._parser = self._init_parser(self.file)

    def has_node(self, node: str) -> bool:
        return node in self._parser

    def get_float(self, node: str, option: str) -> float:
        return self._get_from_parser(node, option, self._to_float)

    def get_int(self, node: str, option: str) -> int:
        return self._get_from_parser(node, option, self._to_int)

    def get_string(self, node: str, option: str) -> str:
        return self._get_from_parser(node, option, self._to_string)

    def _get_from_parser(self, node, option: str, callback):
        json_node = self._get_node_from_parser(node)
        result = self._get_option_from_parser(json_node, option)
        return callback(result)

    def _get_option_from_parser(self, node: JsonNode, option: str):
        if not node.has_option(option):
            raise KeyError(f"not found option {option}")
        return node.get(option)

    def _get_node_from_parser(self, node):
        return self._parser[node]

    def _init_parser(self, file: PathTypes) -> DefaultDict[str, JsonNode]:
        data = self._read_json(file, self._encoding)
        filtered = self._filter_json(data)
        return defaultdict(self._default_node, filtered)

    def _filter_json(self, result: dict) -> Dict[str, JsonNode]:
        if not is_dict(result):
            return {}
        return {key: self._default_node(key, value) for key, value in result.items()}

    def _read_json(self, file, encoding: str = None) -> dict:
        result = {}
        if self.is_config_file(file):
            encoding = self._to_encoding(Encoding.UTF_8) if not encoding else encoding
            with open(file, mode="r") as f:
                result = json.load(f, encoding=encoding)
        return result

    def _default_node(self, key: str = None, value=None):
        _key: str = key
        if _key is None:
            _key = uuid4()
        return JsonNode(key, value)
