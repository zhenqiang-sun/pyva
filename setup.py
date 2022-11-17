"""
PyVa-Framework
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setuptools.setup(
    name="pyva-framework",
    version="3.1.17",
    author="Zhenqiang Sun",
    author_email="zhenqiang.sun@gmail.com",
    description="PyVa = Python项目 + Java风格，这是一个工程框架库，包含DB、Redis、MongoDB、JSON等工具和基础服务类。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhenqiang-sun/pyva",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements.replace("\n", " ").split(),
)
