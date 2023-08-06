# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from typing import Callable

from .core import HttpxResponse
from .manager import AsyncHttpManager
from .components import HttpInterceptors, Method, MethodTypes, HttpURL, Options, StrOrUrl, TimoutTypes


class Methods(Enum):
    DELETE = "DELETE"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


class IAsyncHttpBuilder(object):

    def add_cookies(self, key: str, value: str) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_cookies(key, value) -> IAsyncHttpBuilder")

    def add_headers(self, key: str, value: str) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_headers(key, value) -> IAsyncHttpBuilder")

    def add_data(self, key: str, value) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_data(key, value) -> IAsyncHttpBuilder")

    def add_json(self, key: str, value) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_json(key, value) -> IAsyncHttpBuilder")

    def add_params(self, key: str, value) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_params(key, value) -> IAsyncHttpBuilder")

    def add_request_interceptor(self, function: Callable) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_request_interceptor(function) -> IAsyncHttpBuilder")

    def add_response_interceptor(self, function: Callable) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_response_interceptor(function) -> IAsyncHttpBuilder")

    async def request(self, *args, **kwargs) -> HttpxResponse:
        raise NotImplementedError("NotImplemented .request() -> HttpxResponse")


class AsyncHttpBuilder(IAsyncHttpBuilder):

    def __init__(self,
                 method: MethodTypes,
                 url: StrOrUrl,
                 timeout: TimoutTypes = None):
        self._name = "default"
        self._method = Method(method)
        self._url = HttpURL(url)
        self._options = Options(timeout)
        self._interceptors = HttpInterceptors()

    def add_cookies(self, key, value):
        cookies = self._options.cookies
        cookies.add(key, value)
        return self

    def add_data(self, key, value):
        data = self._options.data
        data.add(key, value)
        return self

    def add_headers(self, key, value):
        headers = self._options.headers
        headers.add(key, value)
        return self

    def add_json(self, key, value):
        json = self._options.json
        json.add(key, value)
        return self

    def add_params(self, key, value):
        params = self._options.params
        params.add(key, value)
        return self

    def add_request_interceptor(self, function: Callable):
        request = self._interceptors.request
        return request.add(function)

    def add_response_interceptor(self, function: Callable):
        response = self._interceptors.response
        return response.add(function)

    async def request(self):
        return await self.build_request(
            self._name,
            self._method,
            self._url,
            self._options,
            self._interceptors
        )

    async def build_request(self,
                            name: str,
                            method: Method,
                            url: HttpURL,
                            options: Options,
                            interceptors: HttpInterceptors):
        instance = AsyncHttpManager().get_instance(name)
        async with instance as http:
            if not interceptors.empty():
                http.set_interceptor(interceptors)
            return await http.request(
                method.to_string(),
                url.to_string(),
                options=options
            )
