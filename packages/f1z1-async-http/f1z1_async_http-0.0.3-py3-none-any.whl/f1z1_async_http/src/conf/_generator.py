# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import ReaderFactory

from . import IHttpConfigGenerator, HttpConfig


class HttpConfigGenerator(IHttpConfigGenerator):

    @classmethod
    def generate_from_ini(cls, filename: str, **kwargs):
        reader = ReaderFactory.create(filename)
        return HttpConfig(reader)
