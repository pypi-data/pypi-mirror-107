# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import defaultdict
from enum import Enum

from common.src.conf import BaseReader, ConfigOptions, BaseGenerator
from common.src.conf import ParserFactory, ReaderFactory, GeneratorFactory
from common.src.utils import get_from_allowed, EnumUtil, PathTypes


class _Klass(Enum):
    READER = "reader"
    GENERATOR = "generator"


class ConfigBuilder(object):
    _classes = EnumUtil.create_dict_by_enum(_Klass)
    _extension_names = ["ini"]

    def __init__(self, filename: PathTypes):
        self._parser = ParserFactory.create(filename)
        self._reader_class = BaseReader
        self._options_class = ConfigOptions
        self._generator_class = BaseGenerator

        self._kwargs = defaultdict(dict)

    def set_reader_class(self, reader_class: BaseReader):
        if not ReaderFactory.is_reader_subclass(reader_class):
            raise ValueError(f"reader class need {BaseReader.__name__} subclass, but got {reader_class}")
        self._reader_class = reader_class

    def set_reader_kwargs(self, **kwargs):
        self._update_kwargs(_Klass.READER, **kwargs)

    def get_reader_kwargs(self):
        return self._get_kwargs(_Klass.READER)

    def set_generator_class(self, generator_class: BaseGenerator):
        if not GeneratorFactory.is_generator_subclass(generator_class):
            raise ValueError(f"reader class need {BaseGenerator.__name__} subclass, but got {generator_class}")
        self._generator_class = generator_class

    def set_generator_kwargs(self, **kwargs):
        self._update_kwargs(_Klass.GENERATOR, **kwargs)

    def get_generator_kwargs(self):
        return self._get_kwargs(_Klass.GENERATOR)

    def build(self) -> BaseGenerator:
        reader = self._create_reader()
        generator = self._create_generator(reader)
        return generator

    def _create_reader(self):
        kwargs = self.get_reader_kwargs()
        return ReaderFactory.create(
            self._reader_class,
            self._parser,
            self._options_class,
            **kwargs
        )

    def _create_generator(self, reader: BaseReader):
        kwargs = self.get_generator_kwargs()
        return GeneratorFactory.create(
            subklass=self._generator_class,
            reader=reader,
            **kwargs
        )

    def _update_kwargs(self, key, **kwargs):
        if not kwargs:
            return
        self._get_kwargs(key).update(kwargs)

    def _get_kwargs(self, key: _Klass):
        return self._kwargs[self._allowed_klass(key)]

    def _allowed_klass(self, key: _Klass):
        return get_from_allowed(key, ConfigBuilder._classes)
