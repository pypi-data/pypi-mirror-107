# -*- coding: utf-8 -*-

import setuptools
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

data_folder = Path(".") / "donb_custom_widget" / "data"
data_files = [str(file.absolute()) for file in data_folder.rglob("*")]
data_files.append("py.typed")

setuptools.setup(
    name="donb-custom-widget",
    version="1.1.0",
    author="Don Beberto",
    author_email="bebert64@gmail.com",
    description="Custom widget for Pyside6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_data={"": data_files},
    packages=setuptools.find_packages(where="."),
    install_requires=["Pyside6", "donb-tools",],
)
