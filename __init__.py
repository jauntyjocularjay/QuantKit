import sys

from . import constants
from . import stats

# Provide top-level compatibility aliases for scripts that do `from stats import *`
# while still running as part of the `quantkit` package.
sys.modules.setdefault("constants", constants)
sys.modules.setdefault("stats", stats)