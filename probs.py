import math as Math
import statistics as Statistics
try:
    from .pytils import console  # For package usage
except ImportError:
    import console as console    # For direct script usage
from fractions import Fraction
from enum import Enum
from typing import Literal
from pprint import pprint

console.clear()

UNION = '∪'
INTERSECTION = '∩'
GIVEN = '|'
OUTCOME = 'outcome'
ALL_OUTCOMES = 'all_outcomes'
DESIRED_OUTCOMES = 'desired_outcomes'
FAIR_PROBABILITY = 'fair_probability'
FAIR_COMPLEMENT = 'fair_complement'

class Event(Enum):
    DEPENDENT = 'dependent'
    INDEPENDENT = 'independent'
    MUTUALL_EXCLUSIVE = 'mutually_exlusive'

class FairProbability:
    def __init__(self, outcome_set: set, desired_outcome_set: set):
        if not isinstance(outcome_set, set): raise TypeError(f'{outcome_set} must be a set')
        if not isinstance(desired_outcome_set, set): raise TypeError(f'{desired_outcome_set} must be a set')

        self.all_outcomes = outcome_set
        self.desired_outcomes = desired_outcome_set

    def __str__(self):
        return f'{self.as_dict}'
    
    @property
    def as_dict(self):
        return {
            DESIRED_OUTCOMES: self.all_outcomes,
            ALL_OUTCOMES: self.desired_outcomes,
            FAIR_PROBABILITY: self.fair_probability,
            FAIR_COMPLEMENT: self.fair_complement
        }
    
    @property
    def fair_probability(self):
        return Fraction(len(self.desired_outcomes), len(self.all_outcomes))
    
    @property
    def fair_complement(self):
        return Fraction(len(self.all_outcomes) - len(self.desired_outcomes), len(self.all_outcomes))


# ex. Coin flipping Heads or Tails twice in a row
outcomes = {'th','ht','tt','hh'}
desired_outcomes = {'tt', 'hh'}

cf = FairProbability(outcomes, desired_outcomes)

print(f'desired_outcomes:outcomes => {desired_outcomes}:{outcomes}')
print(f'fair probability + complement = {cf.fair_probability + cf.fair_complement}')
print(f'cloinflip = ')
pprint(cf.as_dict)
