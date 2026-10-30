import pytest
from .constants import VALUE
from .pytilities.validation import (
    InvalidSequenceError,
    NotNumericSequenceError,
    ProhibitedValueError,
    ValueAboveBoundsError,
    ValueBelowBoundsError,
    sequence_are_numbers,
)
from .stats import binom, geom, interquartile_slice, iqs, median_index
from .boxplot import BoxPlot


# --- median_index tests ---

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
def test_iqs_returns_expected_slice():
    '''Test that iqs returns the expected IQR slice for tuple input.'''
    data = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    result = iqs(data)
    expected = (3, 4, 5, 6, 7)
    assert result == expected, f'iqs should return {expected} for tuple input, got {result}'


# --- Error class tests ---
def test_invalid_sequence_error():
    '''Test BoxPlot raises InvalidSequenceError for a None input sequence.'''
    with pytest.raises(InvalidSequenceError, match='expected a'):
        BoxPlot(None) # type: ignore

def test_not_numeric_sequence_error():
    '''Test BoxPlot raises NotNumericSequenceError for non-numeric input.'''
    with pytest.raises(NotNumericSequenceError, match='expected a'):
        BoxPlot([1, 'a', 3, 4])


# --- sequence_are_numbers tests ---
def test_sequence_are_numbers_all_numeric():
    '''Test sequence_are_numbers returns True for all-numeric sequence.'''
    actual = sequence_are_numbers([1, 2.5, 3])
    assert actual is True, f'sequence_are_numbers should return True for all numeric sequence. Expected: True, Actual: {actual}'

def test_sequence_are_numbers_non_numeric():
    '''Test sequence_are_numbers returns False if any element is not numeric.'''
    actual = sequence_are_numbers([1, 'a', 3])
    assert actual is False, f'sequence_are_numbers should return False if any element is not numeric. Expected: False, Actual: {actual}'

def test_sequence_are_numbers_nan_inf():
    '''Test sequence_are_numbers returns False if any element is NaN or infinite.'''
    actual_nan = sequence_are_numbers([1, float('nan'), 3])
    assert actual_nan is False, f'sequence_are_numbers should return False if any element is NaN. Expected: False, Actual: {actual_nan}'
    actual_inf = sequence_are_numbers([1, float('inf'), 3])
    assert actual_inf is False, f'sequence_are_numbers should return False if any element is infinite. Expected: False, Actual: {actual_inf}'


# --- Additional coverage tests ---
def test_median_index_not_numeric():
    '''Test median_index raises NotNumericSequenceError for non-numeric input.'''
    with pytest.raises(NotNumericSequenceError, match='expected a'):
        median_index(['a', 2, 3])

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

def test_boxplot_not_numeric():
    '''Test BoxPlot raises NotNumericSequenceError for non-numeric sequence.'''
    with pytest.raises(NotNumericSequenceError, match='expected a'):
        BoxPlot([1, 'a', 3, 4])

def test_boxplot_too_short():
    '''Test BoxPlot raises ValueError for sequence shorter than 4 elements.'''
    with pytest.raises(ValueError, match='at least length 4'):
        BoxPlot([1, 2, 3])

def test_boxplot_inclusive_method():
    '''Test BoxPlot with inclusive quantile method returns inclusive quartiles.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = BoxPlot(data, quantile_method='inclusive')
    assert bp.q1 == 2.75, f'BoxPlot.q1 should be 2.75 for inclusive quartiles, got {bp.q1}'
    assert bp.q3 == 6.25, f'BoxPlot.q3 should be 6.25 for inclusive quartiles, got {bp.q3}'
    assert bp.median == 4.5, f'BoxPlot.median should remain 4.5, got {bp.median}'




# --- binom tests ---
@pytest.mark.parametrize('p, n, k, expected_value', [
    (0.5, 1, 1, 0.5),
    (0.5, 2, 1, 0.5),
    (0.2, 5, 1, 0.4096),
    (0.7, 3, 2, 0.441),
])
def test_binom_typical(p, n, k, expected_value):
    '''Test binom returns correct probability for typical cases.'''
    result = binom(p, n, k)
    actual = float(result[VALUE])
    assert abs(actual - expected_value) < 1e-6, f'binom({p}, {n}, {k}) should return probability {expected_value}, got {actual}'

def test_binom_invalid_probability():
    '''Test binom raises error for invalid probability.'''
    with pytest.raises(ValueBelowBoundsError, match='less than 1'):
        binom(1.5, 2, 1)
    with pytest.raises(ValueAboveBoundsError, match='greater than 0'):
        binom(-0.1, 2, 1)

def test_binom_invalid_trials():
    '''Test binom raises an error when n_trials is below k_success.'''
    with pytest.raises(ValueAboveBoundsError, match='greater than 2'):
        binom(0.5, 1, 2)

def test_binom_zero_trials_prohibited():
    '''Test binom raises ProhibitedValueError when n_trials is zero.'''
    with pytest.raises(ProhibitedValueError, match='expected 0 not to be any of'):
        binom(0.5, 0, 0)

# --- geom tests ---
@pytest.mark.parametrize('p, k, expected_value', [
    (0.5, 1, 0.5),
    (0.5, 2, 0.25),
    (0.2, 3, 0.128),
    (0.7, 1, 0.7),
])
def test_geom_typical(p, k, expected_value):
    '''Test geom returns correct probability for typical cases (includes_success=True).'''
    result = geom(p, k, includes_success=True)
    actual = float(result[VALUE])
    assert abs(actual - expected_value) < 1e-6, f'geom({p}, {k}) should return probability {expected_value}, got {actual}'

def test_geom_invalid_probability():
    '''Test geom raises error for invalid probability.'''
    with pytest.raises(ValueBelowBoundsError, match='less than 1'):
        geom(1.5, 2)
    with pytest.raises(ValueAboveBoundsError, match='greater than 0'):
        geom(-0.1, 2)

def test_geom_zero_or_one_probability():
    '''Test geom raises error for p=0 or p=1.'''
    with pytest.raises(ProhibitedValueError, match='expected 0 not to be any of'):
        geom(0, 2)
    with pytest.raises(ProhibitedValueError, match='expected 1 not to be any of'):
        geom(1, 2)
        
        