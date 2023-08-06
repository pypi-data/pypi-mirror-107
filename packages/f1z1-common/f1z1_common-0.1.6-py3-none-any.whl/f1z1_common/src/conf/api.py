# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .reader import IniReader, JsonReader
from .builder import ReaderBuilder

from ..utils import Encoding, PathTypes


def create_ini_reader(file: PathTypes,
                      encoding: Encoding = None) -> IniReader:
    builder = ReaderBuilder(file, encoding)
    builder.add_ext_name("int")
    return builder.build()


def create_json_reader(file: PathTypes,
                       encoding: Encoding = Encoding.UTF_8) -> JsonReader:
    builder = ReaderBuilder(file, encoding)
    builder.set_reader(JsonReader)
    builder.add_ext_name("json")
    return builder.build()
