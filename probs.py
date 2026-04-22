import math as Math
import statistics as Statistics
import itertools as Itertools
try:
    from . import console       # For package usage
except ImportError:
    import console as console   # For direct script usage
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Literal, Union
from enum import Enum
from typing import Literal
from pprint import pprint
from validation import *

console.clear()

UNION_SYM = '∪'
INTERSECTION_SYM = '∩'
GIVEN_SYM = '|'
OUTCOME = 'outcome'
ALL_OUTCOMES = 'all_outcomes'
DESIRED_OUTCOMES = 'desired_outcomes'
FAIR_PROBABILITY = 'fair_probability'
FAIR_COMPLEMENT = 'fair_complement'
PROBABILITY = 'probability'
COMPLEMENT = 'complement'

class Event(Enum):
    DEPENDENT = 'dependent'
    INDEPENDENT = 'independent'
    MUTUAL_EXCLUSIVE = 'mutually_exlusive'

@dataclass
class Outcome:
    ''' Outcome is a class for holding data as a building block for probabilities.
    Work In Progress
    '''
    _key: Union[str, int, float]
    _weight: Union[Fraction] # int, None] # TBA

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
    
    def __repr__(self):
        return self.__str__()
    
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

    @property
    def as_dict(self):
        return {self.key: self.weight}

class Probability:
    def __init__(self, sample_space: set):
        Probability.is_set_of_outcomes(sample_space)
        self._sample_space = sample_space
    
    @classmethod
    def is_set_of_outcomes(cls, outcomes):
        validate_as(outcomes, set)

        for x in outcomes:
            validate_as(x, Outcome)

    @property
    def sample_space(self):
        return self._sample_space




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
            DESIRED_OUTCOMES: self.desired_outcomes,
            ALL_OUTCOMES: self.all_outcomes,
            FAIR_PROBABILITY: self.fair_probability,
            FAIR_COMPLEMENT: self.fair_complement
        }
    
    @property
    def fair_probability(self):
        return Fraction(len(self.desired_outcomes), len(self.all_outcomes))
    
    @property
    def fair_complement(self):
        return Fraction(len(self.all_outcomes) - len(self.desired_outcomes), len(self.all_outcomes))


one_six = Fraction(1,6)
one_twenty = Fraction(1,20)
# ex. Coin flipping Heads or Tails twice in a row

def single_fair_outcomes(string:str = 's', number_of_outcomes: int = 6):
    validate_as(string, str)
    validate_as(number_of_outcomes, int)

    return {Outcome(f'{string}{_}', Fraction(1, number_of_outcomes)) for _ in range(1,number_of_outcomes)}

def all_combinations(unique_outcomes: str = 'th', trials: int = 2):
    validate_as(unique_outcomes, str)
    return {''.join(p) for p in Itertools.product(unique_outcomes, repeat=trials)}

outcomes = single_fair_outcomes('s', 20)

print('1d6 outcomes:')
for outcome in sorted(outcomes, key=lambda o: o._key):
    print(outcome)

print(f'coin toss all_combinations: {all_combinations('th', 5)}')



