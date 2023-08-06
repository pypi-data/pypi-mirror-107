# -*- coding: utf-8 -*-

import setuptools
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

data_folder = Path(".") / "donb_gallery" / "data"
data_files = [str(file.absolute()) for file in data_folder.rglob("*")]
data_files.append("py.typed")

setuptools.setup(
    name="donb-gallery",
    version="1.0.2",
    author="Don Beberto",
    author_email="bebert64@gmail.com",
    description="A gallery QWidget for managing objects through tags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_data={"": data_files},
    packages=setuptools.find_packages(where="."),
    install_requires=[
        "Pyside6",
        "donb-custom-widget",
        "donb-tools",
        "donb-config[toml]",
        "peewee",
    ],
    entry_points={
        "pyinstaller40": [
            "hook-dirs = donb_gallery._pyinstaller_hook_dir:get_hook_dirs"
        ]
    },
)
