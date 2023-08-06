# coding: utf-8
from setuptools import setup

setup(
    name='nhl_user_jwt',
    version='1.1.2',
    author_email='ligocz@dingtalk.com',
    url='http://www.nihuola.vip/',
    packages=['nhl_user_jwt'],   # python包
    # py_modules=['nhl_user_jwt'],    # 待打包的单个脚本
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'python-jose>=3.2.0',
        'passlib>=1.7.4',
        'redis>=3.5.2'
    ]
)
