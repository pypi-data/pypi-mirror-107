# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='SuperRPA',
    version='0.0.7',  # 版本
    author='叶狼',
    author_email='yelang97@qq.com',
    description='二次封装 Selenium，并且后期会维护搭载各种文本、csv、xlsx、本地文件等操作。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitee.com/xiaoye_01/super-rpa',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[  # 添加依赖
        'selenium', 'pyperclip', 'openpyxl',
    ]
)
