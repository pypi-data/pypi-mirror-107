# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import defaultdict
from enum import Enum

from f1z1_common import Allowed, AsyncCallbackManager

from . import Interceptors


class InterceptorKeys(Enum):
    REQUEST = "request"
    RESPONSE = "response"


class HttpInterceptors(Interceptors):
    keys = Allowed(InterceptorKeys)

    def __init__(self):
        self._interceptors = defaultdict(AsyncCallbackManager)
        self._request = InterceptorKeys.REQUEST
        self._response = InterceptorKeys.RESPONSE

    @property
    def request(self):
        return self._get_interceptor(self._request)

    @property
    def response(self):
        return self._get_interceptor(self._response)

    def empty(self) -> bool:
        return not self._interceptors

    def _get_interceptor(self, key: InterceptorKeys):
        return self._interceptors[self.keys.get(key)]
