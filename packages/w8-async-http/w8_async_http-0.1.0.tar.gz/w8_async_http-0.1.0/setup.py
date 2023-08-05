# @Time     : 2021/5/25
# @Project  : async-http
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from setuptools import setup, find_packages

_name = "w8_async_http"
_author = "angel"
_author_email = "376355670@qq.com"
_description = "wb of async http"
_py_version = ">=3.7"
_install_requires = [
    "httpx>=0.18.1"
]


def get_long_description():
    long_description = ""
    with open("README.md", mode="r", encoding="utf-8") as rd:
        long_description += rd.read()

    return long_description


setup(
    name=_name,
    version="0.1.0",
    author=_author,
    author_email=_author_email,
    python_requires=_py_version,
    install_requires=_install_requires,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
    ]
)
