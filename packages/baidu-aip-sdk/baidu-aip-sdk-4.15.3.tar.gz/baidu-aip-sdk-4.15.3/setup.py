# -*- coding:utf-8 -*-

from os import path as os_path
from setuptools import setup, find_packages

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename)) as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='baidu-aip-sdk',  # 包名
    python_requires='~=3.4',  # python环境
    version='4.15.3',  # 包的版本
    description="Baidu AIP SDK",  # 包简介，显示在PyPI上
    long_description=read_file('README.md'),  # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author='Baidu',
    author_email='aip@baidu.com',
    url = 'https://github.com/Baidu-AIP',
    # 指定包信息，还可以用find_packages()函数
    packages=[
        'baidu_aip_sdk',
    ],
    install_requires=[
        'requests',
    ],
    include_package_data=False,
    license="MIT",
    keywords = ['baidu', 'aip', 'ocr', 'antiporn', 'nlp', 'face', 'kg', 'speech'],
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
