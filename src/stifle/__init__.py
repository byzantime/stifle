"""stifle — delete comments (and optionally docstrings) from Python code.

Library use::

    from stifle import ALL_TARGETS, strip_source, verify

    stripped = strip_source(src, {"own-line"})
    assert verify(src, stripped, {"own-line"})
"""

from stifle._core import ALL_TARGETS
from stifle._core import DEFAULT_KEEPS
from stifle._core import DOCSTRINGS
from stifle._core import ORPHAN_STRINGS
from stifle._core import OWN_LINE
from stifle._core import TARGETS
from stifle._core import TRAILING
from stifle._core import DocstringViolation
from stifle._core import docstring_violations
from stifle._core import strip_source
from stifle._core import verify

__version__ = "1.0.0"

__all__ = [
    "OWN_LINE",
    "TRAILING",
    "DOCSTRINGS",
    "ORPHAN_STRINGS",
    "ALL_TARGETS",
    "TARGETS",
    "strip_source",
    "verify",
    "DEFAULT_KEEPS",
    "DocstringViolation",
    "docstring_violations",
    "__version__",
]
