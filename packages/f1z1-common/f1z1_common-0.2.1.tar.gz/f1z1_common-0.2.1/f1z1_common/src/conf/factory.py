# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from . import IReaderFactory, IniReader, JsonReader
from ..utils import EncodingTypes, PathUtil


class IniReaderFactory(IReaderFactory):

    @classmethod
    def create(cls, filename: str, encoding: EncodingTypes = None, **kwargs) -> IniReader:
        return IniReader(filename, encoding)


class JsonReaderFactory(IReaderFactory):
    @classmethod
    def create(cls, filename: str, encoding: EncodingTypes = None, **kwargs) -> IniReader:
        return JsonReader(filename, encoding)


class ReaderFactory(IReaderFactory):

    @classmethod
    def create(cls, filename: str, encoding: EncodingTypes = None, **kwargs):
        if cls.is_ini_file(filename):
            return IniReaderFactory.create(filename, encoding)
        elif cls.is_json_file(filename):
            return JsonReaderFactory.create(filename, encoding)
        else:
            raise ValueError(
                f"file ext name error, {filename}"
            )

    @staticmethod
    def is_json_file(filename: str):
        return PathUtil.is_endswith_ext(filename, [".json"])

    @staticmethod
    def is_ini_file(filename: str):
        return PathUtil.is_endswith_ext(filename, [".ini"])
