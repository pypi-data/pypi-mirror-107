# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from configparser import ConfigParser
from functools import partial

from common.src.conf import BaseReader, BaseGenerator, ConfigOptions
from common.src import PathUtil, PathTypes


class IFactory(object):
    """
    工厂接口
    """

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError()


class ParserFactory(IFactory):

    @classmethod
    def create(cls, filename: PathTypes) -> ConfigParser:
        parser = ConfigParser()
        file = PathUtil.to_path(filename)
        if cls.is_config_file(file):
            parser.read(file)
        return parser

    @staticmethod
    def is_config_file(file):
        return PathUtil.is_endswith_ext(file, ReaderFactory._extension_names)


class ReaderFactory(IFactory):
    _extension_names = ["ini"]

    @classmethod
    def create(cls,
               subklass: BaseReader,
               parser: ConfigParser,
               options_klass: ConfigOptions,
               **kwargs) -> BaseReader:
        f = cls._factory(subklass, parser, options_klass)
        return f(**kwargs)

    @classmethod
    def _factory(cls,
                 subklass: BaseReader,
                 parser: ConfigParser,
                 options_klass: ConfigOptions):
        """

        :param subklass:
        :param parser:
        :param options_klass:
        :return:
        """
        klass = BaseReader
        if cls.is_reader_subclass(subklass):
            klass = subklass
        return partial(klass, parser, options_klass)

    @staticmethod
    def is_reader_subclass(klass):
        return issubclass(klass, BaseReader)


class GeneratorFactory(IFactory):

    @classmethod
    def create(cls,
               subklass: BaseGenerator,
               reader: BaseReader, **kwargs) -> BaseGenerator:
        f = cls._factory(subklass, reader)
        return f(**kwargs)

    @staticmethod
    def is_reader(reader):
        return isinstance(reader, BaseReader)

    @staticmethod
    def is_generator_subclass(klass):
        return issubclass(klass, BaseGenerator)

    @classmethod
    def _factory(cls, subklass: BaseGenerator, reader: BaseReader):
        if not cls.is_reader(reader):
            raise ValueError(f"reader need a BaseReader instance, but got {type(reader)}")
        klass = BaseGenerator
        if cls.is_generator_subclass(subklass):
            klass = subklass
        return partial(subklass, reader=reader)
