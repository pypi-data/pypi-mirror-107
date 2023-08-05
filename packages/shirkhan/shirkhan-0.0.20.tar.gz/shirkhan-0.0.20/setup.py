import re

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("shirkhan/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

"""
备注:

easy_install的配置文件是~/.pydistutils.cfg，在其中指定index-url即可避免访问官方PyPI。 以下以阿里源为例。
[easy_install]
index-url=http://mirrors.aliyun.com/pypi/simple/
"""
setup(
    name="shirkhan",
    version=version,
    author="shirkhan",
    author_email="uybabbage@hotmail.com",
    description="shirkhan tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ishirkhan",
    packages=find_packages(),
    install_requires=[
        "pycryptodome",
        "xlrd",
        "openpyxl",
    ],
    extras_require={
        'voice_annotations': ['praatio', 'pydub']
    },
    tests_require=[
        'pytest'
    ],
    setup_requires=[
        'wheel',
        'twine'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
