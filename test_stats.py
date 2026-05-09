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


def assert_raises_expected(callable_obj, expected_exception_type, context_message):
    actual_exception = None
    try:
        callable_obj()
    except Exception as exc:
        actual_exception = exc
    assert isinstance(actual_exception, expected_exception_type), (
        f'{context_message}. Expected exception type: {expected_exception_type.__name__}, '
        f'Actual: {type(actual_exception).__name__ if actual_exception is not None else "No exception"}'
    )


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
def test_iqs_equivalence():
    '''Test that iqs returns the same result as interquartile_slice for the same input.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = iqs(data)
    expected = interquartile_slice(data)
    assert result == expected, f'iqs should equal interquartile_slice for the same input. Expected: {expected}, Actual: {result}'


# --- Error class tests ---
def test_invalid_sequence_error():
    '''Test InvalidSequenceError can be raised and has correct message.'''
    actual_exception = InvalidSequenceError()
    assert isinstance(actual_exception, InvalidSequenceError), f'Expected exception type InvalidSequenceError, Actual: {type(actual_exception).__name__ if actual_exception is not None else "No exception"}'
    assert 'expected' in str(actual_exception), f"Expected exception message to contain 'expected', Actual: {str(actual_exception)}"

def test_not_numeric_sequence_error():
    '''Test NotNumericSequenceError can be raised and has correct message.'''
    actual_exception = NotNumericSequenceError()
    assert isinstance(actual_exception, NotNumericSequenceError), f'Expected exception type NotNumericSequenceError, Actual: {type(actual_exception).__name__ if actual_exception is not None else "No exception"}'
    assert 'expected a' in str(actual_exception), f"Expected exception message to contain 'expected a', Actual: {str(actual_exception)}"


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
    assert_raises_expected(
        lambda: median_index(['a', 2, 3]),
        NotNumericSequenceError,
        'median_index should raise for non-numeric input',
    )

# --- BoxPlot class tests ---
def test_boxplot_as_dict_and_str():
    '''Test BoxPlot.as_dict() and __str__() for correct output and keys.'''
    # Typical case
    data = [1, 2, 3, 4, 5, 6]
    bp = BoxPlot(data)
    d = bp.as_dict()
    # Check all expected keys are present
    for key in ['min', 'q1', 'median', 'q2', 'q3', 'max', 'data_list', 'iqr', 'range']:
        assert key in d, f"BoxPlot.as_dict() should contain key '{key}'. Expected: key present, Actual keys: {list(d.keys())}"
    # Check __str__ output contains expected values
    s = str(bp)
    assert str(bp.min) in s, f'BoxPlot.__str__ should include min value. Expected substring: {bp.min}, Actual string: {s}'
    assert str(bp.q1) in s, f'BoxPlot.__str__ should include q1 value. Expected substring: {bp.q1}, Actual string: {s}'
    assert str(bp.median) in s, f'BoxPlot.__str__ should include median value. Expected substring: {bp.median}, Actual string: {s}'
    assert str(bp.q3) in s, f'BoxPlot.__str__ should include q3 value. Expected substring: {bp.q3}, Actual string: {s}'
    assert str(bp.max) in s, f'BoxPlot.__str__ should include max value. Expected substring: {bp.max}, Actual string: {s}'

def test_boxplot_properties():
    '''Test BoxPlot properties: range, iqr, iqr_balance, whisker_balance.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = BoxPlot(data)
    # Test range
    expected_range = bp.max - bp.min
    assert bp.range == expected_range, f'BoxPlot.range should be max - min. Expected: {expected_range}, Actual: {bp.range}'
    # Test iqr
    expected_iqr = bp.q3 - bp.q1
    assert bp.iqr == expected_iqr, f'BoxPlot.iqr should be q3 - q1. Expected: {expected_iqr}, Actual: {bp.iqr}'
    # Test iqr_balance
    left = bp.median - bp.q1
    right = bp.q3 - bp.median
    expected_balance = (left - right) / bp.iqr
    actual_iqr_balance_delta = abs(bp.iqr_balance - expected_balance)
    assert actual_iqr_balance_delta < 1e-9, f'BoxPlot.iqr_balance should match formula. Expected: {expected_balance}, Actual: {bp.iqr_balance}'
    # Test whisker_balance
    left_w = bp.q1 - bp.min
    right_w = bp.max - bp.q3
    expected_wb = (left_w - right_w) / bp.range
    actual_whisker_balance_delta = abs(bp.whisker_balance - expected_wb)
    assert actual_whisker_balance_delta < 1e-9, f'BoxPlot.whisker_balance should match formula. Expected: {expected_wb}, Actual: {bp.whisker_balance}'

def test_boxplot_not_numeric():
    '''Test BoxPlot raises NotNumericSequenceError for non-numeric sequence.'''
    assert_raises_expected(
        lambda: BoxPlot([1, 'a', 3, 4]),
        NotNumericSequenceError,
        'BoxPlot should raise for non-numeric sequence',
    )

def test_boxplot_too_short():
    '''Test BoxPlot raises ValueError for sequence shorter than 4 elements.'''
    assert_raises_expected(
        lambda: BoxPlot([1, 2, 3]),
        ValueError,
        'BoxPlot should raise for sequence shorter than 4',
    )

def test_boxplot_inclusive_method():
    '''Test BoxPlot with inclusive quantile method.'''
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = BoxPlot(data, quantile_method='inclusive')
    assert isinstance(bp, BoxPlot), f'BoxPlot should be created with inclusive method. Expected type: BoxPlot, Actual: {type(bp).__name__}'




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
    assert_raises_expected(
        lambda: binom(1.5, 2, 1),
        ValueBelowBoundsError,
        'binom should raise for p > 1',
    )
    assert_raises_expected(
        lambda: binom(-0.1, 2, 1),
        ValueAboveBoundsError,
        'binom should raise for p < 0',
    )

def test_binom_invalid_trials():
    '''Test binom raises error for invalid n_trials.'''
    assert_raises_expected(
        lambda: binom(0.5, 0, 0),
        ProhibitedValueError,
        'binom should raise for invalid n_trials',
    )

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
    assert_raises_expected(
        lambda: geom(1.5, 2),
        ValueBelowBoundsError,
        'geom should raise for p > 1',
    )
    assert_raises_expected(
        lambda: geom(-0.1, 2),
        ValueAboveBoundsError,
        'geom should raise for p < 0',
    )

def test_geom_zero_or_one_probability():
    '''Test geom raises error for p=0 or p=1.'''
    assert_raises_expected(
        lambda: geom(0, 2),
        ProhibitedValueError,
        'geom should raise for p=0',
    )
    assert_raises_expected(
        lambda: geom(1, 2),
        ProhibitedValueError,
        'geom should raise for p=1',
    )
        
        