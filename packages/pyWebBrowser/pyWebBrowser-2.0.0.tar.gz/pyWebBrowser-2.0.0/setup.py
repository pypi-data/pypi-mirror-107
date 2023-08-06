# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name = 'pyWebBrowser',
    version = '2.0.0',
    author = 'Yogurt_cry',
    author_email = 'ben.2001@foxmail.com',
    description = '基于 C# 开发的浏览器控制工具。整合提供了浏览器控制、键鼠控制、屏幕截图、剪切板控制等常用 API',
    url = 'https://gitee.com/Yogurt_cry/pyWebBrowser',
    packages = setuptools.find_packages(
        include = ['pyWebBrowser', 'pyWebBrowser.*'],
    ),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires = ['pythonnet'],
    python_requires = '>=3',
    include_package_data = True,
)
