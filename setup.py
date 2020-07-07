#!/usr/bin/env python
import os
import re

from setuptools import setup, find_namespace_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description(long_description_file):
    """
    Read long description from file.
    """
    with open(long_description_file, encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name="meow.webs",
    version=get_version("meow/webs"),
    url="https://github.com/aachurin/meow.webs",
    license="MIT",
    description="Expressive WEB apiS",
    long_description=get_long_description("README.md"),
    long_description_content_type="text/markdown",
    author="Andrey Churin",
    maintainer="Andrey Churin",
    maintainer_email="aachurin@gmail.com",
    packages=find_namespace_packages(include=["meow.*"]),
    package_data={"meow.webs": ["py.typed"]},
    install_requires=["jinja2", "werkzeug", "whitenoise", "meow.di", "meow.validators"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # entry_points={
    #     'console_scripts': [
    #         'stark=stark:main'
    #     ],
    # },
)
