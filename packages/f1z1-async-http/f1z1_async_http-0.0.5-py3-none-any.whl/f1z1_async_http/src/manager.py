# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_http.f1z1_async_http.src.core import IAsyncHttpManager, IAsyncHttp, AsyncHttpFactory
from f1z1_http.f1z1_async_http.src.conf import HttpConfigGenerator

CONF_FILE = "config.ini"
DEFAULT = "default"
DEFAULT_CONF = HttpConfigGenerator.generate_from_ini(CONF_FILE)


class AsyncHttpManager(IAsyncHttpManager):
    __shared = {DEFAULT: AsyncHttpFactory.create(DEFAULT_CONF)}

    def __init__(self):
        self._instances = AsyncHttpManager.__shared

    def get_instance(self, name: str = DEFAULT, **kwargs):
        if not self.has(name):
            self[name] = self._create(name)
        return self._instances[name]

    def _create(self, name: str):
        config = self._get_config(CONF_FILE, name)
        return AsyncHttpFactory.create(config)

    def _get_config(self, filename: str = "config.ini", node: str = DEFAULT):
        config = HttpConfigGenerator.generate_from_ini(filename)
        config.set_node(node)
        return config

    def __getitem__(self, item):
        return self._instances.get(item, DEFAULT)

    def __setitem__(self, name: str, instance: IAsyncHttp) -> None:
        if not self._is_async_client(instance):
            raise ValueError(
                f"value need AsyncHttp instance, but got {type(instance).__name__}"
            )
        self._instances[name] = instance

    def has(self, name: str):
        return name in self._instances

    def _is_async_client(self, value):
        return isinstance(value, IAsyncHttp)
