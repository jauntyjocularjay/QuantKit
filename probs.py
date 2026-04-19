import math as Math
import statistics as Statistics
try:
    from . import console  # For package usage
except ImportError:
    import console         # For direct script usage
from typing import Literal
from pprint import pprint

UNION = '∪'
INTERSECTION = '∩'
GIVEN = '|'

class Probability:
    def __init__(self, outcome_set: set):
        if not isinstance(outcome_set, set): raise TypeError('outcome must be a set')

        self.outcomes = outcome_set





