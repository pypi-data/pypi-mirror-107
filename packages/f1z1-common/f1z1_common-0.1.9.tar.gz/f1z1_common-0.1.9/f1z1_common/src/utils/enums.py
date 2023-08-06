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
    def unenum_value(cls, any_or_member: Enum) -> Any:
        return any_or_member.value if is_enum(any_or_member) else any_or_member

    @classmethod
    def unenum_name(cls, any_or_member: Enum) -> str:
        return any_or_member.name if is_enum(any_or_member) else any_or_member

    @classmethod
    def unenum_to_dict(cls, enum_subclass: Enum) -> dict:
        if not is_enum_subclass(enum_subclass):
            raise ValueError(f"enum klass not Enum subclass, got {type(enum_subclass).__name__}")
        unenum_value = cls.unenum_value
        return {item: unenum_value(item) for _, item in enumerate(enum_subclass)}
