import math as Math
from enum import Enum
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Union
from pytilities.validation import *

class outcome:
    ''' Outcome represents a single possible result in a probability space, with an associated key and weight.

    This class is designed as a building block for probability and statistics calculations, encapsulating
    the concept of an outcome in an experiment or random process. Each Outcome has a unique key (such as
    a label, number, or identifier) and a weight, which is a Fraction representing its probability or relative
    likelihood. The class enforces type safety for both key and weight, and provides methods for validation,
    comparison, and representation.

    Attributes:
        * _key (str | int | float): The unique identifier for the outcome. Must not be inf or nan if float.
        * _weight (Fraction): The weight or probability associated with the outcome. This value MUST be less than
          abs(1) => |1|. Negative values are acceptable.

    Methods:
        key_is_valid(key): Validates that the key is an acceptable type and value.
        weight_is_fraction(weight): Ensures the weight is a Fraction.
        is_outcome(other): Checks if another object is an Outcome instance.
        as_dict: Returns the outcome as a dictionary {key: weight}.

    Example:
        >>> from fractions import Fraction
        >>> o = Outcome('heads', Fraction(1, 2))
        >>> print(o)
        { 'heads': 1/2 }
        >>> o.as_dict
        {'heads': Fraction(1, 2)}
    '''
    _key: Union[str, int, float, bool, Enum]
    _weight: Fraction

    def __init__(self, key: Union[str, int, float, bool, Enum], weight: Union[Fraction, int, float] = 1):

        outcome.key_is_valid(key)
        validate_as(weight, (Fraction, int, float))

        self._key = key

        if isinstance(weight, float):
            validate_float(weight)
            if abs(weight) > 1:
                weight = 1 / weight
            self._weight = Fraction(weight)

        elif isinstance(weight, int):
            if weight == 0:
                self._weight = Fraction(0, 1)
            else:
                self._weight = Fraction(1 / weight)

        else:
            self._weight = weight


    @classmethod
    def key_is_valid(cls, key):
        validate_as(key, (str, int, float, bool, Enum))
        if isinstance(key, float): validate_float(key)

    @classmethod
    def weight_is_fraction(cls, weight):
        if not isinstance(weight, Fraction):
            raise TypeError(f'{{weight: {weight}}} must be a fraction')

    @classmethod
    def is_outcome(cls, other):
        if not isinstance(other, outcome): raise TypeError(f'{{{other}}} is not an outcome')

    def __str__(self):
        return f'{{ \'{self._key}\': {self._weight} }}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        outcome.is_outcome(other)
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
        outcome.weight_is_fraction(weight)
        self._weight = weight

    @property
    def as_dict(self):
        return {self.key: self.weight}