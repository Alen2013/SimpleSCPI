#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SimpleSCPI - 简单易用的 SCPI 仪器控制工具

一个基于 PyQt5 的图形界面工具，用于控制和测试 SCPI 兼容的测试仪器。
支持多种连接方式（TCP/IP、USB、串口），提供可视化的命令管理界面。
"""

__version__ = "1.0.0"
__author__ = "SimpleSCPI Contributors"
__email__ = "your.email@example.com"
__license__ = "MIT"

# 项目信息
PROJECT_NAME = "SimpleSCPI"
PROJECT_DESCRIPTION = "一个简单易用的 SCPI 仪器控制工具"
PROJECT_URL = "https://github.com/yourusername/SimpleSCPI"

# 版本信息
VERSION_INFO = tuple(map(int, __version__.split('.')))

# 导出的公共接口
__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "PROJECT_NAME",
    "PROJECT_DESCRIPTION",
    "PROJECT_URL",
    "VERSION_INFO",
] 