# -*- coding: utf-8 -*-

"""
Defines :
 The MyCustomGalleryWidget class.

"""

from typing import Optional
from PySide6 import QtWidgets

from donb_custom_widget.my_custom_widget import MyCustomWidget
from donb_gallery.models.gallery_models import GalleryModels


class MyCustomGalleryWidget(MyCustomWidget):

    """
    Derived from MyCustomWidget, to allow to pass down the "models" object to all
    widgets (in addition to config).

    """

    models: GalleryModels

    @classmethod
    def create_widget(
        cls, parent: Optional[QtWidgets.QWidget] = None
    ) -> MyCustomWidget:
        # create_widget is a factory method, and should therefore be allowed
        # to access protected members of the class.
        # pylint: disable = protected-access
        widget = super().create_widget(parent)
        if widget._has_parent():
            widget._copy_attribute_from_parent("models")
            widget._copy_attribute_from_parent("config")
        return widget
