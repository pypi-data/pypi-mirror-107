# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Any

from ..validator.is_validators import is_dict


def get_from_allowed(key: Any, allowed_props: dict) -> Any:
    allowed = {} if not is_dict(allowed_props) else allowed_props
    result = allowed.get(key)
    if result is None:
        raise KeyError(f"not found allowed key from {allowed}")
    return result
