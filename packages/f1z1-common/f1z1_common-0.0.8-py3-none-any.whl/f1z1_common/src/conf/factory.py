# @Time     : 2021/5/28
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from functools import partial

from .reader import AllowedOptions, AbstractConfigReader
from ..utils import ExtensionNameList, PathTypes
from ..validator.is_validators import is_iterable, is_list


class IFactory(object):

    @classmethod
    def create(cls, *args, **kwargs) -> AbstractConfigReader:
        raise NotImplementedError("")


class ReaderFactory(IFactory):

    @classmethod
    def create(cls,
               subclass: AbstractConfigReader,
               file: PathTypes,
               options: AllowedOptions,
               extension_names: ExtensionNameList = None,
               **kwargs) -> AbstractConfigReader:
        f = cls._factory(
            subclass, file, options, extension_names
        )
        return f(**kwargs)

    @classmethod
    def _factory(cls,
                 subclass: AbstractConfigReader,
                 file: PathTypes,
                 options: AllowedOptions,
                 extension_names: ExtensionNameList = None):
        if not cls.is_reader_subclass(subclass):
            raise ValueError(f"need a AbstractConfigReader subclass, but got {type(subclass).__name__}")
        klass = subclass
        return partial(
            klass,
            file,
            options=options,
            extension_names=cls.to_extension_names(extension_names)
        )

    @staticmethod
    def to_extension_names(extension_names: ExtensionNameList = None) -> list:
        if is_list(extension_names):
            return extension_names
        elif is_iterable(extension_names):
            return list(extension_names)
        else:
            return []

    @staticmethod
    def is_reader_subclass(subclass):
        return issubclass(subclass, AbstractConfigReader)
