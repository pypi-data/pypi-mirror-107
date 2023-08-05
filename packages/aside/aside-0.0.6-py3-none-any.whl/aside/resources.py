"""Manages the package resource files."""

try:
    from importlib.abc import Traversable
except ImportError:
    from importlib_resources.abc import Traversable

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

__all__ = [
    "Traversable",
    "root",
    "get_svg",
]

root: Traversable = files(__package__) / "_resources"
"""The root traversable resource location.

See :any:`importlib_resources<importlib_resources:using>`
and :py:mod:`importlib.resources` for more information.

:meta hide-value:
"""


def get_svg(name: str) -> bytes:
    """Find and load an svg resource specified by ``name``.

    Args:
        name: The name of the svg resource without the file extension.

    Returns:
        The contents of the resource, suitable to be loaded with
        :py:meth:`PyQt5.QtGui.QPixmap.loadFromData`.

    ToDo:
        Take the current ``LOCALE`` into account:

        * look for ``root/locale/name`` first
        * then fallback to ``root/name``

    ToDo:
        Generate/interpolate SVGs on the fly, possibly with system caching.
    """
    return (root / (name + ".svg")).read_bytes()
