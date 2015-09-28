# coding:utf-8
__author__ = '613108'


def listSplit(ls, n):
    """
    # 列表分割函数，参数说明：
    # ls:待分割列表
    # n:分割份数
    :param ls:
    :param n:
    :return:
    """
    if not isinstance(ls, list) or not isinstance(n, int):
        return None
    elif n <= 0 or n > len(ls):
        return None
    elif n == len(ls):
        return [[item] for item in ls]
    else:
        x = len(ls) / n
        y = len(ls) % n
        is_return = []
        for i in range(0, (n - 1) * x, x):
            is_return.append(ls[i:i + x])
        is_return.append(ls[(n - 1) * x:])
    return is_return
