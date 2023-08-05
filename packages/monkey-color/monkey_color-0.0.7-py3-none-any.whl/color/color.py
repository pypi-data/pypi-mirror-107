
# Author: 猴子
# Date: 2021-05-23 15:09:28
# LastEditTime: 2021-05-24 13:47:12
# FilePath: /code/color/color.py
import re
__all__ = [
    "ANSI_COLOR_NAMES",
    "color",
]

back = {
    # 黑色
    "black": 40,
    # 红色
    "red": 41,
    # 绿色
    "green": 42,
    # 黃色
    "yellow": 43,
    # 蓝色
    "blue": 44,
    # 紫红色
    "Fuchsia": 45,
    # 青蓝色
    "cyan": 46,
    # 白色
    "white": 47,
}

txt = {
    # 黑色
    "black": 30,
    # 红色
    "red": 31,
    # 绿色
    "green": 32,
    # 黃色
    "yellow": 33,
    # 蓝色
    "blue": 33,
    # 紫红色
    "Fuchsia": 35,
    # 青蓝色
    "cyan": 36,
    # 白色
    "white": 37,
}


def color(*args):
    string = ""
    for arg in args:
        string += arg
    for _type in [(txt, ""), (back, "back_")]:
        for i in list(_type[0]):
            string = re.sub(f"\[(({_type[1]+i})+)\]",
                            f"\033[{_type[0][i]}m", string)
    string = string.replace("[/]", "\033[0m")
    return string
