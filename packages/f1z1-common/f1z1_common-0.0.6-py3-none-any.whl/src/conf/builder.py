# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum

from common.src.conf import AllowedOptions, AbstractConfigReader, IniReader, JsonReader, ReaderFactory
from common.src.utils import EnumUtil, ExtensionNameList, get_from_allowed, PathTypes
from common.src.validator.is_validators import is_string, is_enum_subclass


class ReaderType(Enum):
    INI = IniReader
    JSON = JsonReader


class ReaderBuilder(object):
    _classes = EnumUtil.create_dict_by_enum(ReaderType)

    def __init__(self,
                 filename: PathTypes,
                 options: AllowedOptions,
                 extension_names: ExtensionNameList = None):
        self._filename = filename
        self._options = options
        self._extension_names = [] if not extension_names else extension_names

        self._reader_class = ReaderType.INI
        self._kwargs = {}

    def build(self) -> AbstractConfigReader:
        return ReaderFactory.create(
            self._get_allowed_class(self._reader_class),
            self._filename,
            self._options,
            self._extension_names,
            **self._kwargs
        )

    def set_reader(self, reader_class: ReaderType):
        if not self._is_allowed_class(reader_class):
            return self
        self._set_allowed_class(reader_class)
        return self

    def set_options(self, options: AllowedOptions):
        if not is_enum_subclass(options):
            return self
        self._options = options
        return self

    def set_kwargs(self, **kwargs):
        if not kwargs:
            return self
        self._kwargs.update(kwargs)
        return self

    def add_extension_name(self, extension_name: str):
        if not is_string(extension_name):
            return self
        self._extension_names.append(extension_name)
        return self

    def _get_allowed_class(self, reader_class: ReaderType) -> AbstractConfigReader:
        return get_from_allowed(reader_class, ReaderBuilder._classes)

    def _set_allowed_class(self, reader_class: ReaderType) -> None:
        self._reader_class = reader_class

    def _is_allowed_class(self, reader_class: ReaderType):
        return reader_class in ReaderBuilder._classes
