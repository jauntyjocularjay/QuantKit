import math as Math
import statistics as Statistics
try:
    from . import console  # For package usage
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



class Outcome:
    _key: str

    def __init__(self, key, weight: Fraction = Fraction(1,1)):
        Outcome.key_is_valid(key)
        Outcome.weight_is_fraction(weight)

        object.__setattr__(self, '_key', key)
        self._weight = weight

    @classmethod
    def key_is_valid(cls, key):
        if isinstance(key, float) and (Math.isinf(key) or Math.isnan(key)):
            raise TypeError(f'{{key: {key}}} cannot be {Math.inf} or {Math.nan}')
        elif isinstance(key, (str, int, bool)):
            return
        else:
            raise TypeError(f'{{key: {key}}} must be a string, int, float, bool (not inf/nan)')

    @classmethod
    def weight_is_fraction(cls, weight):
        if not isinstance(weight, Fraction):
            raise TypeError(f'{{weight: {weight}}} must be a fraction')

    @classmethod
    def is_outcome(cls, other):
        if not isinstance(other, Outcome): raise TypeError(f'{{{other}}} is not an outcome')

    def __str__(self):
        return f'{{ \'{self._key}\': {self._weight} }}'
    
    def __eq__(self, other):
        Outcome.is_outcome(other)
        return self.key == other.key
    
    def __hash__(self):
        return hash(self.key)

    @property
    def key(self):
        return self._key

    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, weight: Fraction):
        Outcome.weight_is_fraction(weight)
        self._weight = weight

class Probability:
    def __init__(self, outcomes: set):
        Probability.is_set_of_outcomes(outcomes)
        
        self._outcomes = outcomes
    
    @classmethod
    def is_set_of_outcomes(cls, outcomes):
        if not isinstance(outcomes, set): raise TypeError(f'Probability.outcomes must be a set')

        for x in outcomes:
            if not isinstance(x, Outcome): raise TypeError('Probability.outcomes may only contains Outcomes')





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
