# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from typing import Any

from ..validator.is_validators import is_enum, is_enum_subclass


class EnumUtil(object):

    @classmethod
    def to_value(cls, enums: Enum) -> Any:
        if not is_enum(enums):
            raise ValueError(f"enum need Enum instance, but got {type(enums).__name__}")
        return enums.value

    @classmethod
    def create_dict_by_enum(cls, enum_klass: Enum) -> dict:
        if not is_enum_subclass(enum_klass):
            raise ValueError(f"enum klass not Enum subclass, got {type(enum_klass).__name__}")
        to_value = cls.to_value
        return {item: to_value(item) for _, item in enumerate(enum_klass)}
