# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import AbstractConfReader, IReaderBuilder
from .reader import IniReader
from ..utils import Encoding, ExtensionNameList, PathTypes
from ..validator.is_validators import is_none, is_string


class ReaderBuilder(IReaderBuilder):

    def __init__(self, file: PathTypes, encoding: Encoding = None):
        self._file = file
        self._ext_names: ExtensionNameList = []
        self._encoding = encoding
        self._reader_class = IniReader

    def set_reader(self, reader_class: AbstractConfReader) -> None:
        if not self._is_subclass(reader_class):
            raise ValueError(f"reader class need AbstractConfReader subclass, but got {type(reader_class).__name__}")
        self._reader_class = reader_class

    def add_ext_name(self, ext_name: str) -> None:
        if not is_string(ext_name):
            raise ValueError(f"file ext name need string, but got {type(ext_name).__name__}")
        self._ext_names.append(ext_name)

    def build(self):
        if is_none(self._reader_class):
            raise ValueError(f"reader class is not None")
        return self._reader_class(
            self._file, self._ext_names, self._encoding
        )

    def _is_subclass(self, reader):
        return issubclass(reader, AbstractConfReader)
