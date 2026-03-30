"""Package initializer for netzplan_gui_version.

This file allows the modules in the directory to be imported as a package
in unit tests and other contexts.  The existing GUI code inserts the
directory on ``sys.path`` and continues to import ``netzplan_core`` etc.
Adding an ``__init__`` file does not change that behaviour but makes it
possible to write tests using proper package imports if desired.
"""

__version__ = "0.1"# version nummer könnte hier angepasst werden
