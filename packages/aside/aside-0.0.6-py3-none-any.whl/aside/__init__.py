"""Personal task tracker with the organization of tasks in the form of queues."""

from . import version
from .version import version as __version__

# Note: The reason why these imports from . are surrounded by try-except here is
#       that this __init__ file will be imported during build/install and so our
#       package dependencies might not be installed yet.
try:
    from . import boilerplate, gui, resources
    from .gui import main
except ImportError:  # pragma: no cover
    boilerplate = None
    gui = None
    main = None
    resources = None

__all__ = [
    "version",
    "__version__",
    "boilerplate",
    "gui",
    "resources",
    "main",
]
