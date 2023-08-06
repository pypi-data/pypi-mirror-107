# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from pathlib import Path

from f1z1_common import PathUtil

BASE_PATH = Path(__file__).parents[0].resolve()


def get_config_file(filename: str) -> Path:
    return PathUtil.get_path_from_base_dir(BASE_PATH, filename)
