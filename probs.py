import itertools as Itertools
from fractions import Fraction
from typing import Union, Type
from pytilities.validation import *
from constants import *
import math as Math
from pprint import pprint



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

def geom(p: Union[Fraction, int, float], trials: int = 0, includes_success: bool = True):
    validate_as(p, (Fraction, int, float))
    if isinstance (p, float): validate_float(p)
    validate_is_greater_than(p, 0)
    validate_against(p,0)

    p = Fraction(p)
    q = Fraction(p.denominator - p.numerator, p.denominator)
    value = p * pow(q,trials - 1) if includes_success else p * pow(q, trials)
    mean = Fraction(p.denominator, p.numerator) if includes_success else Fraction(1-p, p)
    variance = Fraction(q, p**2) 

    return {
        VALUE: {
            FRAC: value,
            FLOAT: float(value)
        },
        MEAN: {
            FRAC: mean,
            FLOAT: float(mean)},
        SDEV: {
            FRAC: f'sqrt({variance})',
            FLOAT: float(Math.sqrt(variance))
        }
    }

result =  geom(Fraction(5,16), 9)
pprint(result)

result =  geom(Fraction(5,16), 9, False)
pprint(result)



