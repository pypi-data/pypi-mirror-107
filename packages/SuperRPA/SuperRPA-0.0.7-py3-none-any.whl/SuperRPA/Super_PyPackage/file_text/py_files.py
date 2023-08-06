# -*- coding: utf-8 -*-
"""
封装操作文件功能：查
"""
import os


def check_file(route):
    """
    :param route: 如：\\name，就可以获取到 name文件夹下的所有文件，包括文件夹。
    :return:
    """
    if '\\' != route[0]:
        return None
    filepath = os.getcwd() + route
    path = []
    for dirpath, dirnames, filenames in os.walk(filepath):
        for names in filenames:
            path.append(os.path.join(dirpath, names))
    return path
