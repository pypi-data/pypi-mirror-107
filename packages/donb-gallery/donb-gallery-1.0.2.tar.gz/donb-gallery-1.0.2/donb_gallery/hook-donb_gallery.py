# -*- coding: utf-8 -*-

"""
PyInstaller's hook.
"""


import donb_gallery
from pathlib import Path
gallery_path = Path(donb_gallery.__file__).parent / "data"

config_path = gallery_path / "config_gallery.toml"
datas = [(str(config_path), "data")]

ui_files_path = gallery_path / "ui_files"
datas += [(str(ui_files_path), "data/ui_files")]

icons_path = gallery_path / "icons"
datas += [(str(icons_path), "data/icons")]
