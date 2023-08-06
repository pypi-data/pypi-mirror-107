# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.comf
from collections import defaultdict, namedtuple
from enum import Enum

from f1z1_common import Allowed

from . import IOptional, IOptions, TimoutTypes

Opt = namedtuple("Opt", ["name", "option"])


class Option(IOptional):

    def __init__(self):
        self._options = []

    def to_dict(self):
        if self.empty():
            return {}
        return dict(self._options)

    def add(self, name, option) -> None:
        opt = Opt(name, option)
        self._options.append(opt)

    def empty(self):
        return not self._options


class OptionKeys(Enum):
    COOKIES = "cookies"
    DATA = "data"
    HEADERS = "headers"
    JSON = "json"
    PARAMS = "params"


class Options(IOptions):
    keys = Allowed(OptionKeys)

    def __init__(self, timeout: TimoutTypes = None):
        self._timeout = timeout
        self._options = defaultdict(Option)

    @property
    def cookies(self):
        return self._get_from_optional(OptionKeys.COOKIES)

    @property
    def data(self):
        return self._get_from_optional(OptionKeys.DATA)

    @property
    def headers(self):
        return self._get_from_optional(OptionKeys.HEADERS)

    @property
    def json(self):
        return self._get_from_optional(OptionKeys.JSON)

    @property
    def params(self):
        return self._get_from_optional(OptionKeys.PARAMS)

    @property
    def timeout(self):
        return self._timeout

    def empty(self) -> bool:
        return all([not self._options, not self._timeout])

    def _get_from_optional(self, options: OptionKeys):
        return self._options[self.keys.get(options)]
