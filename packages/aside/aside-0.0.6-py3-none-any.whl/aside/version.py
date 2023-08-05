"""Manages the package version information."""

import os
import typing

import pkg_resources as pkg

from . import _version

__all__ = [
    "get_version",
    "base_version",
    "version",
]


def get_version(
    commit_tag: typing.Optional[str] = None,
    short_sha: typing.Optional[str] = None,
) -> str:
    """Get the `version` of the currently installed aside package.

    When the ``commit_tag`` and ``short_sha`` values are not specified, the current
    version is inferred from :any:`pkg_resources<setuptools:pkg_resources>` or
    `base_version`. If the package was not built under official CI, then the string
    ``.post0+installed.from.source`` is appended to the version number.

    Args:
        commit_tag:
            The tag of the currently building commit. It is checked to be matching with
            the `base_version`, otherwise a `RuntimeError` is raised to abort the build.
        short_sha:
            The sha of the currently building commit. If no ``commit_tag`` was
            specified, then this is a development build and the ``short_sha`` is
            appended to the current version using the ``.post0+sha`` extension.

    Returns:
        The resulting version string.
    """
    if commit_tag:
        if commit_tag != base_version:
            raise RuntimeError(
                "Attempting CI build with mismatching package version ({}) "
                "and CI tag version ({}).".format(base_version, commit_tag)
            )
        return base_version

    if short_sha:
        # PEP 440 compliant way to include commit SHA in package version.
        # We use "post" instead of "pre", because we want this version to be
        # considered newer, than the previous release version.
        # (1.0.0.post0+... > 1.0.0 > 1.0.0.pre0+...)
        return base_version + ".post0+sha" + short_sha

    # If our package is currently installed, query pkg_resources for a more
    # accurate version description. This allows us to install development
    # (x.y.z.post0+sha) builds and have accurate version info.
    try:
        return pkg.get_distribution(__name__.split(".")[0]).version
    except pkg.DistributionNotFound:  # pragma: no cover
        return base_version + ".post0+installed.from.source"


base_version: str = _version.__version__
"""Specifies the semantic version of the package."""

version: str = get_version(
    commit_tag=os.environ.get("CI_COMMIT_TAG", None),
    short_sha=os.environ.get("CI_COMMIT_SHORT_SHA", None),
)
"""Specifies the exact version of the currently installed aside package.

This value is determined from the values of `base_version`, the
:any:`pkg_resources <setuptools:pkg_resources>` distribution version of the current
package and the ``CI_COMMIT_TAG`` and ``CI_COMMIT_SHORT_SHA`` environment variables.

Unlike `base_version`, `version` may include extra information for development versions
and source installations. See `get_version` for more info.

:meta hide-value:
"""
