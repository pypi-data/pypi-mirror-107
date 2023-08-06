# @Time     : 2021/5/26
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from typing import AnyStr, Union

from common.src.utils.enums import EnumUtil
from common.src.validator.is_validators import (
    is_bytes,
    is_bytearray,
    is_enum,
    is_string
)

StringOrBytesOrByteArray = Union[AnyStr, bytearray]


class Encoding(Enum):
    """
    默认编码方式
    """
    ISO_8859_1 = "ISO-8859-1"
    UTF_8 = "utf-8"


class StringsUtil(object):

    @classmethod
    def anystr_to_string(cls,
                         str_or_bytes: AnyStr,
                         encoding: Encoding = Encoding.UTF_8) -> str:
        """
        string or bytes to string
        :param str_or_bytes:
        :param encoding:
        :return:
        """
        string: str = ""
        if is_string(str_or_bytes):
            string = str_or_bytes
        elif is_bytes(str_or_bytes):
            string = str_or_bytes.decode(encoding)
        else:
            raise ValueError(f"need a string or bytes, but got {type(str_or_bytes).__name__}")
        return string

    @classmethod
    def anystr_to_bytes(cls,
                        str_or_bytes_barray: StringOrBytesOrByteArray) -> bytes:
        """
        string, bytes, bytearray to bytes
        :param str_or_bytes_barray:
        :return:
        """
        bstring: bytes = b""
        if any([
            is_bytes(str_or_bytes_barray),
            is_bytearray(str_or_bytes_barray)
        ]):
            bstring = str_or_bytes_barray
        elif is_string(str_or_bytes_barray):
            bstring = str_or_bytes_barray.encode()
        else:
            raise ValueError(f"need string, bytes, bytearray, but got {type(str_or_bytes_barray).__name__}")
        return bstring

    @staticmethod
    def to_encoding(encoding: Encoding) -> str:
        result: str = None
        to_value = EnumUtil.to_value
        if not is_enum(encoding):
            result = to_value(Encoding.UTF_8)
        else:
            result = to_value(encoding)
        return result
