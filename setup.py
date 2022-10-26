"""
PyVa-Framework
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyva-framework",
    version="3.1.0",
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
    install_requires=[
        "fastapi==0.85.0",
        "uvicorn==0.18.3",
        "SQLAlchemy==1.4.41",
        "PyMySQL==1.0.2",
        "sqlacodegen==2.3.0",
        "redis==4.3.4",
        "requests==2.28.1",
        "pyhumps==3.7.3",
        "nacos-sdk-python==0.1.8",
        "PyYAML==6.0",
        "python-multipart==0.0.5",
        "pymongo==4.2.0",
        "orjson==3.8.0",
    ],
)
