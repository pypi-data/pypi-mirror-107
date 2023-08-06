# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
"""
conf module interfaces
"""
from abc import ABCMeta, abstractmethod
from ..utils import EncodingTypes, ExtensionNameList, PathTypes, PathUtil, StringsUtil
from ..validator.is_validators import (
    is_any_string,
    is_float,
    is_int,
    is_list,
    is_none,
    is_number,
    is_string
)


class AbstractConfReader(metaclass=ABCMeta):
    """
    config reader abc class
    """

    def __init__(self,
                 file: PathTypes,
                 ext_names: ExtensionNameList = None,
                 encoding: EncodingTypes = None):
        self._file = file
        self._ext_names = [] if not is_list(ext_names) else ext_names
        self._encoding = encoding

    @property
    def file(self):
        return self._file

    @abstractmethod
    def has_node(self, node) -> bool:
        raise NotImplementedError("NotImplemented .has_node(node) -> bool")

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

    def is_config_file(self, file: PathTypes) -> bool:
        return PathUtil.is_endswith_ext(file, self._ext_names)

    def _to_encoding(self, encoding: EncodingTypes = None):
        if is_none(encoding):
            return None
        return StringsUtil.to_encoding(encoding)


class IReaderBuilder(object):

    def set_reader(self, reader_class: AbstractConfReader) -> None:
        raise NotImplementedError("NotImplemented set_reader(reader) -> None")

    def add_ext_name(self, ext_name: str) -> None:
        raise NotImplementedError("NotImplemented .add_ext_name(ext_name) -> None")

    def build(self) -> AbstractConfReader:
        raise NotImplementedError("NotImplementedError .build() -> AbstractConfReader")
