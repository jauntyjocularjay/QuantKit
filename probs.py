import math as Math
import statistics as Statistics
import itertools as Itertools
from outcome import outcome as Outcome
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Literal, Union
from enum import Enum
from typing import Literal
from pprint import pprint
from pytilities import console
from pytilities.validation import *
from constants import *


console.clear()

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

def single_fair_outcomes(string:str = 's', number_of_outcomes: int = 6):
    validate_as(string, str)
    validate_as(number_of_outcomes, int)

    return {outcome(f'{string}{_}', Fraction(1, number_of_outcomes)) for _ in range(1,number_of_outcomes)}

def all_combinations(unique_outcomes: str = 'th', trials: int = 2):
    validate_as(unique_outcomes, str)
    return {''.join(p) for p in Itertools.product(unique_outcomes, repeat=trials)}

outcomes = single_fair_outcomes('s', 20)

one_six = Fraction(1,6)
one_twenty = Fraction(1,20)

# ex. Coin flipping Heads or Tails twice in a row
print('1d6 outcomes:')
for outcome in sorted(outcomes, key=lambda o: o._key):
    print(outcome)

print(f'coin toss all_combinations: {all_combinations('th', 5)}')



