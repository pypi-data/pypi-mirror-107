#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
 
setup(
  name = "nonebot_plugin_rua",
  version = "0.1.2",
  keywords = ("nonebot2"),
  license = "MIT Licence",
 
  url = "https://github.com/Zeta-qixi/nonebot_plugin_rua",
  author = "Zeta",
  author_email = "1019289695@qq.com",
 
  packages = find_packages(),
  include_package_data = True,
  platforms = "any",
  install_requires = ["PIL"]
)