import pytest # type: ignore
from fractions import Fraction
# from .constants import ( VALUE )
from .pytilities.assert_helpers import (
    assert_approx_equal,
    assert_raises_expected,
)
from .pytilities.validation import (
    InvalidSequenceError,
    InvalidTypeError,
    NotNumericSequenceError,
    ProhibitedValueError,
    ValueAboveBoundsError,
    ValueBelowBoundsError,
    sequence_are_numbers,
)
from .stats import (
    binom,
    geom,
    geom_mean,
    geom_var,
    geoh,
    interquartile_slice,
    iqs,
    median_index,
    nck,
    pois,
)
from .boxplot import BoxPlot

# --- Error class tests ---
def test_not_numeric_sequence_error():
    '''Test BoxPlot raises NotNumericSequenceError for non-numeric input.'''
    with pytest.raises(NotNumericSequenceError):
        BoxPlot([1, 'a', 3, 4])


def test_invalid_sequence_error():
    '''Test BoxPlot raises InvalidSequenceError for a None input sequence.'''
    with pytest.raises(InvalidSequenceError):
        BoxPlot(None) # type: ignore

# --- BoxPlot class tests ---
def test_boxplot_as_dict_and_str():
    '''Test BoxPlot.as_dict() and __str__() for exact output on a known dataset.'''
    data = [1, 2, 3, 4, 5, 6]
    bp = BoxPlot(data)
    d = bp.as_dict()
    expected_dict = {
        'min': 1,
        'q1': 1.75,
        'median': 3.5,
        'q2': 3.5,
        'q3': 5.25,
        'max': 6,
        'tukey_fence': {'min': -3.5, 'max': 10.5},
        'data_list': [1, 2, 3, 4, 5, 6],
        'outliers': [],
        'iqr': 3.5,
        'range': 5,
    }
    assert d == expected_dict, f'BoxPlot.as_dict() should return {expected_dict}, got {d}'
    s = str(bp)
    expected_str = 'boxplot:    min * 1 ---- q1 [ 1.75     median | 3.5     q3 ] 5.25 ---- max * 6]'
    assert s == expected_str, f'BoxPlot.__str__ should return {expected_str}, got {s}'

def test_boxplot_properties():
    '''Test BoxPlot properties against exact expected values for a fixed dataset.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = BoxPlot(data)
    assert bp.min == 1, f'BoxPlot.min should be 1, got {bp.min}'
    assert bp.q1 == 2.25, f'BoxPlot.q1 should be 2.25, got {bp.q1}'
    assert bp.median == 4.5, f'BoxPlot.median should be 4.5, got {bp.median}'
    assert bp.q3 == 6.75, f'BoxPlot.q3 should be 6.75, got {bp.q3}'
    assert bp.max == 8, f'BoxPlot.max should be 8, got {bp.max}'
    assert bp.iqr == 4.5, f'BoxPlot.iqr should be 4.5, got {bp.iqr}'
    assert bp.range == 7, f'BoxPlot.range should be 7, got {bp.range}'
    assert bp.iqr_balance == 0.0, f'BoxPlot.iqr_balance should be 0.0, got {bp.iqr_balance}'
    assert bp.whisker_balance == 0.0, f'BoxPlot.whisker_balance should be 0.0, got {bp.whisker_balance}'

def test_boxplot_too_short():
    '''Test BoxPlot raises ValueError for sequence shorter than 4 elements.'''
    with pytest.raises(ValueError):
        BoxPlot([1, 2, 3])

def test_boxplot_inclusive_method():
    '''Test BoxPlot with inclusive quantile method returns inclusive quartiles.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = BoxPlot(data, quantile_method='inclusive')
    assert bp.q1 == 2.75, f'BoxPlot.q1 should be 2.75 for inclusive quartiles, got {bp.q1}'
    assert bp.q3 == 6.25, f'BoxPlot.q3 should be 6.25 for inclusive quartiles, got {bp.q3}'
    assert bp.median == 4.5, f'BoxPlot.median should remain 4.5, got {bp.median}'
