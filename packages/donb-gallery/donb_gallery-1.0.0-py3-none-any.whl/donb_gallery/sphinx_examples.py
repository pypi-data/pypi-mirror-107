# -*- coding: utf-8 -*-
"""
Examples of what's possible and not with sphinx and autodoc_typehints.

In the text part of a docstring, almost anything goes :
    - as a class :class:`str`
    - as an object :obj:`str`

Object and class don't appear to make much difference...
    - :class:`peewee.Model`
    - :class:`PySide2.QtWidgets.QWidget`
    - :class:`QtWidgets.QWidget`
    - :class:`QWidget`


Other ways to make links :
    - `google <http://google.com>`__
    - :class:`Config <gallery.config_gallery.config_gallery.Config>`
    - :class:`peewee:peewee.Model`
    - :class:`my model <peewee:peewee.Model>`
    - `my model <peewee:peewee.Model>`__

"""

from dataclasses import dataclass
from PySide6 import QtWidgets
import peewee
from donb_gallery.widgets.grid import TabWidget

MODULE_VAR: peewee.SqliteDatabase
"""A Module level variable."""


def function(a: peewee.SqliteDatabase, b: int) -> str:
    """Function docstring."""
    return a + str(b)


class my_class(TabWidget):
    """
    Class docstring. If types are provided in the docstring, they will be taken as
    priority 1. If not, the ones from the __init__ function will be taken.
    It is possible to use markdown notation in the docstring.
    The var "d" is initiated in the __init__ method, but isn't documented, and doesn't
    appear anywhere.

    Parameters
    ----------

    a: :class:`int`
        A string

    b:
        An integer

    Attributes
    ----------
    e:
        The type is given in the __init__ function, but e isn't documented.
    f:
        Type and documentation are present in the __init__ method.
    """

    CLASS_VAR: str = "class variable"
    """A class variable initialized."""

    CLASS_VAR_2: QtWidgets.QWidget
    """A class variable without an initial value."""

    def __init__(self, a: str, b: int):
        self.a = a
        self.b = b
        self.c: str = "a var"
        """c is documented via its own docstring inside the __init__ function."""
        self.d: int = 12
        self.e: str = "haha"
        self.f: str = "nothing"
        """f also has its own docstring inside the __init__ function."""

    def method_type_hints(self, a: str, b: int) -> str:
        """Method docstring."""
        return self.a + a + str(b)

    def method_type_docstring(self, a, b):
        """
        Method docstring.

        Parameters
        ----------
        a: :class:`str`
            A string
        b: :class:`int`
            An integer

        Returns
        -------
        str
            The result
        """
        return self.a + a + str(b)

    def method_type_both_mixed(self, a: str, b: int) -> str:
        """
        In that case, the description comes from the docstring and the types from the
        type hints. I haven't yet found a way to put the result description only in the
        docstring. If there is only one line, it is mistaken for the result type and
        is taken instead of the type hint.

        Parameters
        ----------
        a:
            A string
        b:
            An integer

        Returns
        -------
        str:
            The result
        """
        return self.a + a + str(b)

    def method_type_both_full(self, a: str, b: int) -> str:
        """
        In that case, the type comes from the docstring.

        Parameters
        ----------
        a: :class:`int`
            A string
        b: :class:`str`
            An integer

        Returns
        -------
        int
            The result
        """
        return self.a + a + str(b)


@dataclass
class MyDataclass:
    """
    Class docstring. Type hints from the docstring are priority 1

    Only parameters with their own docstring appear a second time. The var "c", not
    documented anywhere, still appears in the list of parameters.

    Parameters
    ----------
    a: :obj:`str`
        An integer
    b:
        A string
    e:
        A variable documented twice
    """

    a: int
    b: str
    c: peewee.Model
    d: QtWidgets.QWidget
    """d is documented via its own docstring, appears last in the documentation."""
    e: str
    """e is a documented variable."""
