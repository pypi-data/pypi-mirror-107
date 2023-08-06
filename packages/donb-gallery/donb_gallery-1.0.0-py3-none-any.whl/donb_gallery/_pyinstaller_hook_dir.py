# -*- coding: utf-8 -*-

"""
Entry point for PyInstaller's hook.
"""
from typing import List

from donb_tools.functions import get_package_folder


# pylint: disable=missing-function-docstring
def get_hook_dirs() -> List[str]:
    package_folder = get_package_folder()
    return [str(package_folder.parent.absolute())]
