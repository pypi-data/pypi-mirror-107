# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import AbstractCallbackManager
from ..validator import check_function, check_async_function


class CallbackManager(AbstractCallbackManager):

    def check(self, value):
        return check_function(value)

    def notify(self, *args, **kwargs):
        for cb in self:
            try:
                cb(*args, **kwargs)
            except Exception as e:
                raise e


class AsyncCallbackManager(AbstractCallbackManager):

    def check(self, value):
        return check_async_function(value)

    async def async_notify(self, *args, **kwargs):
        async for cb in self:
            try:
                await cb(*args, **kwargs)
            except Exception as e:
                raise e

    async def __aiter__(self):
        if not self.empty():
            for _, cb in enumerate(self.callbacks):
                yield cb
