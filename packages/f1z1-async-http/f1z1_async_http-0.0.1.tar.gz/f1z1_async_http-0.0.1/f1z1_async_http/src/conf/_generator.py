# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import ReaderFactory

from . import IHttpConfigGenerator, HttpConfig
from .. import get_config_file


class HttpConfigGenerator(IHttpConfigGenerator):

    @classmethod
    def generate_from_ini(cls, filename: str, **kwargs):
        file = get_config_file(filename)
        reader = ReaderFactory.create(file)
        return HttpConfig(reader)
