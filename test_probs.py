

import pytest
from fractions import Fraction
from .outcome import outcome as Outcome
from .pytilities.validation import *

@pytest.mark.parametrize("bad_key,desc", [
    (float('inf'), "float('inf')"),
    (float('nan'), "float('nan')"),
])
def test_key_is_valid_inf_nan(bad_key, desc):
    '''key_is_valid should raise ProhibitedValueError for inf/nan.'''
    with pytest.raises(ProhibitedValueError, match="not to be any of"):
        Outcome.key_is_valid(bad_key)

def test_key_is_valid_list():
    '''key_is_valid should raise InvalidTypeError for list input.'''
    with pytest.raises(Exception, match="expected"):
        Outcome.key_is_valid([1,2,3])

@pytest.mark.parametrize("valid_key", ['a', 1, True])
def test_key_is_valid_valid_types(valid_key):
    '''key_is_valid should not raise for str, int, bool.'''
    Outcome.key_is_valid(valid_key)

def test_weight_is_fraction_int():
    '''weight_is_fraction should raise TypeError for int input.'''
    with pytest.raises(TypeError, match="must be a fraction"):
        Outcome.weight_is_fraction(1)

def test_weight_is_fraction_fraction():
    '''weight_is_fraction should not raise for Fraction input.'''
    Outcome.weight_is_fraction(Fraction(1,2))

def test_is_outcome_non_outcome():
    '''is_outcome should raise TypeError for non-Outcome input.'''
    with pytest.raises(TypeError, match="is not an outcome"):
        Outcome.is_outcome(123)

def test_is_outcome_valid():
    '''is_outcome should not raise for Outcome input.'''
    Outcome.is_outcome(Outcome('a'))
