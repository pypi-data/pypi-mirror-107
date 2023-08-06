# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="donb-tools",
    version="1.0.1",
    author="Don Beberto",
    author_email="bebert64@gmail.com",
    description="Common functions and types to reuse across personal projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_data={"": ["py.typed"]},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.8",
)
