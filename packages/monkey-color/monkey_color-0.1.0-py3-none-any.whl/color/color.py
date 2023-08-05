
# Author: 猴子
# Date: 2021-05-23 15:09:28
# LastEditTime: 2021-05-25 18:16:31
# FilePath: /code/color/color.py
import re

__all__ = [
    "_txt",
    "_back",
    "color",
    "rgb",
]

_txt = {
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

_back = {
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


def color(*args):
    string = ""
    for arg in args:
        string += arg
    string = string.replace("[/]", "\033[0m")
    args = [i.replace(" ", "")
            for i in re.findall(r"\[([-A-Za-z0-9(),_ ]+)\]", string)]
    for i in args:
        for _def in re.findall(r"rgb\(+([0-9,]+)\)+", i):
            data = [int(n) for n in _def.split(",")]
            string = re.sub(f"\[rgb\([ ]*{data[0]}[ ]*,[ ]*{data[1]}[ ]*,[ ]*{data[2]}[ ]*\)\]",
                            rgb(data[0], data[1], data[2]), string)
        for _type in [(_txt, ""), (_back, "back-")]:
            for color in list(_type[0]):
                string = re.sub(f"\[(([ ]*{_type[1]+color}[ ]*)+)\]",
                                f"\033[{_type[0][color]}m", string)
    return string


def rgb(Red, Green, Blue):
    return f"\033[38;2;{Red};{Green};{Blue}m"
