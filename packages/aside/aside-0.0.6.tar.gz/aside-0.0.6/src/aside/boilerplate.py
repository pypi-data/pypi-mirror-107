"""Contains common boilerplate/repetetive code."""

import functools
from typing import TYPE_CHECKING, List

import attr
import attrs_strict

__all__ = [
    "attrs",
    "attrib",
    "singleton",
]


def set_default_attribs(
    cls: type,
    fields: List["Attribute"],
) -> List["Attribute"]:
    """Initialize all fields with kwargs from the default `attrib` preset.

    See :any:`attrs:transform-fields` for more info.
    """
    del cls
    return [f.evolve(**attrib.keywords) for f in fields]


if TYPE_CHECKING:
    from attr import Attribute

    # ToDo: inline these type hints after Python3.6 is deprecated
    attrs: functools.partial[attr.s]
    attrib: functools.partial[attr.ib]


attrs = functools.partial(
    attr.s,
    auto_attribs=True,
    collect_by_mro=True,
    field_transformer=set_default_attribs,
    kw_only=True,
    on_setattr=[
        attr.setters.convert,
        attr.setters.validate,
    ],
)
""":py:func:`attr.s` but with our preferred default kwargs preset."""
attrib = functools.partial(
    attr.ib,
    validator=attrs_strict.type_validator(),
)
""":py:func:`attr.ib` but with our preferred default kwargs preset."""


def singleton(cls: type) -> object:
    """Construct a single instance of the decorated class."""
    try:
        return cls()
    except TypeError as exc:
        if exc.args and exc.args[0].startswith("__init__() missing "):
            raise RuntimeError(
                f"Singleton {cls.__name__} must be default constructible."
            ) from exc
        raise
