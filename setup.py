#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SimpleSCPI 项目打包配置
"""
from setuptools import setup, find_packages

# 读取 README 文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取依赖
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="SimpleSCPI",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个简单易用的 SCPI 仪器控制工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/SimpleSCPI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "simplescpi=src.main:main",
        ],
    },
    package_data={
        "src": ["resources/*", "config/*"],
    },
    include_package_data=True,
    zip_safe=False,
) 