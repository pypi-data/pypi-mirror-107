# -*- coding: utf-8 -*-
"""
自动化操作键盘
"""

import pyperclip


def py_paste():
    """输出复制的内容"""
    return pyperclip.paste()


def py_copy(text):
    """
    复制
    :param text: 需要内容复制到粘贴版
    :return: 复制的内容
    """
    pyperclip.copy(text)  # 复制
    return py_paste()


