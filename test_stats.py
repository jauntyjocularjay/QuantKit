import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from pytilities.validation import sequence_are_numbers, InvalidSequenceError, NotNumericSequenceError
from .stats import *
from .boxplot import *
from pytilities.console import clear
from typing import Literal


clear()

# --- median_index tests ---
import math

@pytest.mark.parametrize(
    'input_list,expected,desc',
    [
        ([1, 2, 3, 4, 5], (2,), 'sorted odd-length list'),
        ([5, 4, 3, 2, 1], (2,), 'unsorted odd-length list'),
        ([10], (0,), 'single-element list'),
        ([1, 2, 3, 4, 5, 6], (2, 3), 'sorted even-length list'),
        ([6, 5, 4, 3, 2, 1], (2, 3), 'unsorted even-length list'),
        ([10, 20], (0, 1), 'two-element list'),
        ([], (), 'empty list'),
        (None, (), 'None input'),
        ([1, 2, 2, 3, 4], (2,), 'odd-length list with duplicates'),
        ([1, 2, 2, 3, 4, 4], (2, 3), 'even-length list with duplicates'),
    ]
)
def test_median_index(input_list, expected, desc):
    '''Test median_index for various cases: odd/even, sorted/unsorted, duplicates, empty, None.'''
    result = median_index(input_list)
    assert result == expected, f'median_index should return {expected} for {desc}, got {result}\n'


# --- iqr_slice tests ---
@pytest.mark.parametrize(
    'input_list,expected,desc',
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], [3, 4, 5, 6, 7], 'odd-length list'),
        ([1, 2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6], 'even-length list'),
    ]
)
def test_iqr_slice_typical(input_list, expected, desc):
    '''Test interquartile_slice returns correct slice for typical odd/even-length lists.'''
    result = interquartile_slice(input_list)
    assert result == expected, f'iqr_slice should return {expected} for {desc}, got {result}'

@pytest.mark.parametrize('input_list,desc', [([], 'empty list'), (None, 'None input')])
def test_iqr_slice_empty_none(input_list, desc):
    '''Test interquartile_slice returns None for empty or None input.'''
    result = interquartile_slice(input_list)
    assert result is None, f'iqr_slice should return None for {desc}, got {result}'

def test_iqr_slice_non_numeric():
    '''Test interquartile_slice raises TypeError for non-numeric input.'''
    with pytest.raises(TypeError):
        interquartile_slice([1, 'a', 3])


# --- iqs tests ---
def test_iqs_equivalence():
    '''Test that iqs returns the same result as interquartile_slice for the same input.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = iqs(data)
    expected = interquartile_slice(data)
    assert result == expected, 'iqs should return the same result as interquartile_slice for the same input'


# --- Error class tests ---
def test_invalid_sequence_error():
    '''Test InvalidSequenceError can be raised and has correct message.'''
    with pytest.raises(InvalidSequenceError, match='expected'):
        raise InvalidSequenceError()

def test_not_numeric_sequence_error():
    '''Test NotNumericSequenceError can be raised and has correct message.'''
    with pytest.raises(NotNumericSequenceError, match='real numbers'):
        raise NotNumericSequenceError()


# --- sequence_are_numbers tests ---
def test_sequence_are_numbers_all_numeric():
    '''Test sequence_are_numbers returns True for all-numeric sequence.'''
    assert sequence_are_numbers([1, 2.5, 3]), 'sequence_are_numbers should return True for all numeric sequence'

def test_sequence_are_numbers_non_numeric():
    '''Test sequence_are_numbers returns False if any element is not numeric.'''
    assert not sequence_are_numbers([1, 'a', 3]), 'sequence_are_numbers should return False if any element is not numeric'

def test_sequence_are_numbers_nan_inf():
    '''Test sequence_are_numbers returns False if any element is NaN or infinite.'''
    assert not sequence_are_numbers([1, float('nan'), 3]), 'sequence_are_numbers should return False if any element is NaN'
    assert not sequence_are_numbers([1, float('inf'), 3]), 'sequence_are_numbers should return False if any element is infinite'


# --- Additional coverage tests ---
def test_median_index_not_numeric():
    '''Test median_index raises NotNumericSequenceError for non-numeric input.'''
    with pytest.raises(NotNumericSequenceError):
        median_index(['a', 2, 3])

def test_sequence_are_numbers_none():
    '''Test sequence_are_numbers raises InvalidSequenceError for None input.'''
    with pytest.raises(InvalidSequenceError):
        sequence_are_numbers(None)


# --- BoxPlot class tests ---
def test_boxplot_as_dict_and_str():
    '''Test BoxPlot.as_dict() and __str__() for correct output and keys.'''
    # Typical case
    data = [1, 2, 3, 4, 5, 6]
    bp = BoxPlot(data)
    d = bp.as_dict()
    # Check all expected keys are present
    for key in ['min', 'q1', 'median', 'q2', 'q3', 'max', 'data_list', 'iqr', 'range']:
        assert key in d, f'BoxPlot.as_dict() should contain key \'{key}\''
    # Check __str__ output contains expected values
    s = str(bp)
    assert str(bp.min) in s, 'BoxPlot.__str__ should include min value'
    assert str(bp.q1) in s, 'BoxPlot.__str__ should include q1 value'
    assert str(bp.median) in s, 'BoxPlot.__str__ should include median value'
    assert str(bp.q3) in s, 'BoxPlot.__str__ should include q3 value'
    assert str(bp.max) in s, 'BoxPlot.__str__ should include max value'

def test_boxplot_properties():
    '''Test BoxPlot properties: range, iqr, iqr_balance, whisker_balance.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = BoxPlot(data)
    # Test range
    assert bp.range == bp.max - bp.min, 'BoxPlot.range should be max - min'
    # Test iqr
    assert bp.iqr == bp.q3 - bp.q1, 'BoxPlot.iqr should be q3 - q1'
    # Test iqr_balance
    left = bp.median - bp.q1
    right = bp.q3 - bp.median
    expected_balance = (left - right) / bp.iqr
    assert abs(bp.iqr_balance - expected_balance) < 1e-9, 'BoxPlot.iqr_balance should match formula'
    # Test whisker_balance
    left_w = bp.q1 - bp.min
    right_w = bp.max - bp.q3
    expected_wb = (left_w - right_w) / bp.range
    assert abs(bp.whisker_balance - expected_wb) < 1e-9, 'BoxPlot.whisker_balance should match formula'

def test_boxplot_invalid_sequence():
    '''Test BoxPlot raises InvalidSequenceError for non-sequence input.'''
    with pytest.raises(InvalidSequenceError):
        BoxPlot(None)

def test_boxplot_not_numeric():
    '''Test BoxPlot raises NotNumericSequenceError for non-numeric sequence.'''
    with pytest.raises(NotNumericSequenceError):
        BoxPlot([1, 'a', 3, 4])

def test_boxplot_too_short():
    '''Test BoxPlot raises ValueError for sequence shorter than 4 elements.'''
    with pytest.raises(ValueError):
        BoxPlot([1, 2, 3])

def test_boxplot_inclusive_method():
    '''Test BoxPlot with inclusive quantile method.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = BoxPlot(data, quantile_method='inclusive')
    assert isinstance(bp, BoxPlot), 'BoxPlot should be created with inclusive method'


