# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from httpx import AsyncClient, URL, Timeout, Limits

from . import IAsyncHttpFactory, AsyncHttp, Messages
from ..conf import IHttpConfig


class AsyncHttpFactory(IAsyncHttpFactory):

    @classmethod
    def create(cls, config: IHttpConfig, **kwargs) -> AsyncHttp:
        client = cls._create_async_client_from(config)
        messages = Messages()
        return AsyncHttp(client, messages)

    @classmethod
    def _create_async_client_from(cls, config: IHttpConfig) -> AsyncClient:
        return AsyncClient(
            base_url=cls._create_base_url(config),
            limits=cls._create_limits(config),
            timeout=cls._create_timeout(config)
        )

    @classmethod
    def _create_base_url(cls, config: IHttpConfig) -> URL:
        return URL(config.base_url)

    @classmethod
    def _create_timeout(cls, config: IHttpConfig) -> Timeout:
        return Timeout(config.timeout)

    @classmethod
    def _create_limits(cls, config: IHttpConfig) -> Limits:
        return Limits(
            max_connections=config.max_connection,
            max_keepalive_connections=config.max_keepalive
        )
