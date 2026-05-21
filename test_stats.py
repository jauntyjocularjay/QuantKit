import pytest # type: ignore
from fractions import Fraction
from .constants import *
from .pytilities.pytest_helpers import (
    assert_approx_equal,
    assert_mapping_has_keys,
    assert_raises_expected,
    assert_starts_with,
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
from .stats import binom, geom, geoh, interquartile_slice, iqs, median_index, nck, pois
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


def test_iqr_slice_invalid_sequence_error():
    '''Test interquartile_slice raises InvalidSequenceError for non-sequence input.'''
    assert_raises_expected(
        lambda: interquartile_slice(123), # type: ignore
        InvalidSequenceError,
        'interquartile_slice should raise InvalidSequenceError for non-sequence input',
    )


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
    with pytest.raises(InvalidSequenceError):
        BoxPlot(None) # type: ignore

def test_not_numeric_sequence_error():
    '''Test BoxPlot raises NotNumericSequenceError for non-numeric input.'''
    with pytest.raises(NotNumericSequenceError):
        BoxPlot([1, 'a', 3, 4])


# --- sequence_are_numbers tests ---
@pytest.mark.parametrize('data,expected', [
    ([1, 2.5, 3], True),
    ([1, 'a', 3], False),
    ([1, float('nan'), 3], False),
    ([1, float('inf'), 3], False),
])
def test_sequence_are_numbers(data, expected):
    '''Test sequence_are_numbers truthiness across valid and invalid numeric sequences.'''
    actual = sequence_are_numbers(data)
    assert actual is expected, (
        f'sequence_are_numbers should return {expected} for {data}. Actual: {actual}'
    )


# --- Additional coverage tests ---
def test_median_index_not_numeric():
    '''Test median_index raises NotNumericSequenceError for non-numeric input.'''
    with pytest.raises(NotNumericSequenceError):
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
    assert_approx_equal(
        actual,
        expected_value,
        f'binom({p}, {n}, {k}) should return probability {expected_value}',
        abs_tol=1e-6,
    )

def test_binom_invalid_probability():
    '''Test binom raises error for invalid probability.'''
    assert_raises_expected(
        lambda: binom(1.5, 2, 1),
        ValueAboveBoundsError,
        'binom should raise ValueAboveBoundsError when probability is above 1',
    )
    assert_raises_expected(
        lambda: binom(-0.1, 2, 1),
        ValueBelowBoundsError,
        'binom should raise ValueBelowBoundsError when probability is below 0',
    )

def test_binom_invalid_trials():
    '''Test binom raises an error when n_trials is below k_success.'''
    assert_raises_expected(
        lambda: binom(0.5, 1, 2),
        ValueBelowBoundsError,
        'binom should raise ValueBelowBoundsError when n_trials is below k_success',
    )

def test_binom_zero_trials_prohibited():
    '''Test binom raises ProhibitedValueError when n_trials is zero.'''
    assert_raises_expected(
        lambda: binom(0.5, 0, 0),
        ProhibitedValueError,
        'binom should raise ProhibitedValueError when n_trials is zero',
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
    assert_approx_equal(
        actual,
        expected_value,
        f'geom({p}, {k}) should return probability {expected_value}',
        abs_tol=1e-6,
    )
    std_dev_payload = result[STD_DEV]
    assert_mapping_has_keys(
        std_dev_payload,
        (FRAC_STR, FLOAT),
        f'geom({p}, {k}) std-dev payload should include required keys',
    )
    assert isinstance(std_dev_payload[FRAC_STR], str), f'geom({p}, {k}) should return STD_DEV[{FRAC_STR!r}] as a string, got {type(std_dev_payload[FRAC_STR]).__name__}'
    assert_starts_with(
        std_dev_payload[FRAC_STR],
        'math.sqrt(Fraction(',
        f'geom({p}, {k}) should output python-syntax sqrt Fraction string',
    )

def test_geom_invalid_probability():
    '''Test geom raises error for invalid probability.'''
    assert_raises_expected(
        lambda: geom(1.5, 2),
        ValueAboveBoundsError,
        'geom should raise ValueAboveBoundsError when probability is above 1',
    )
    assert_raises_expected(
        lambda: geom(-0.1, 2),
        ValueBelowBoundsError,
        'geom should raise ValueBelowBoundsError when probability is below 0',
    )

def test_geom_zero_or_one_probability():
    '''Test geom raises strict-bound errors for p=0 or p=1.'''
    assert_raises_expected(
        lambda: geom(0, 2),
        ValueBelowBoundsError,
        'geom should raise ValueBelowBoundsError for p=0',
    )
    assert_raises_expected(
        lambda: geom(1, 2),
        ValueAboveBoundsError,
        'geom should raise ValueAboveBoundsError for p=1',
    )


# --- nck tests ---
@pytest.mark.parametrize('n_trials,k_success,expected', [
    (5, 2, Fraction(10, 1)),
    (6, 0, Fraction(1, 1)),
    (6, 6, Fraction(1, 1)),
])
def test_nck_typical(n_trials, k_success, expected):
    '''Test nck returns expected exact binomial coefficient values.'''
    actual = nck(n_trials, k_success)
    assert actual == expected, f'nck({n_trials}, {k_success}) should return {expected}, got {actual}'


@pytest.mark.parametrize('n_trials,k_success', [
    ('5', 2),
    (5, 2.2),
])
def test_nck_invalid_types(n_trials, k_success):
    '''Test nck raises InvalidTypeError when arguments are not integers.'''
    assert_raises_expected(
        lambda: nck(n_trials, k_success),
        InvalidTypeError,
        f'nck should raise InvalidTypeError for non-int inputs ({n_trials}, {k_success})',
    )


def test_nck_k_greater_than_n_raises():
    '''Test nck raises ValueBelowBoundsError when k_success is greater than n_trials.'''
    assert_raises_expected(
        lambda: nck(3, 4),
        ValueBelowBoundsError,
        'nck should raise ValueBelowBoundsError when k_success exceeds n_trials',
    )


# --- geoh tests ---
def test_geoh_typical_probability():
    '''Test geoh returns expected hypergeometric probability for a standard case.'''
    actual = geoh(5, 5, 4, 2)
    expected = Fraction(10, 21)
    assert actual == expected, f'geoh(5, 5, 4, 2) should return {expected}, got {actual}'


@pytest.mark.parametrize('pop_i,pop_b,n_trials,k_success,expected_error', [
    (5, 5, 2, 3, ValueBelowBoundsError),
    (5, 5, 4, 0, ValueBelowBoundsError),
    (0, 5, 4, 1, ValueBelowBoundsError),
    (5, 0, 4, 1, ValueBelowBoundsError),
])
def test_geoh_invalid_bounds(pop_i, pop_b, n_trials, k_success, expected_error):
    '''Test geoh raises bounds errors for invalid populations/trials/success values.'''
    assert_raises_expected(
        lambda: geoh(pop_i, pop_b, n_trials, k_success),
        expected_error,
        (
            'geoh should raise a bounds error for invalid inputs '
            f'({pop_i}, {pop_b}, {n_trials}, {k_success})'
        ),
    )


# --- pois tests ---
def test_pois_typical_probability():
    '''Test pois computes expected Poisson PMF for a typical safe input.'''
    actual = pois(2, 3)
    expected = 0.22404180765538775
    assert_approx_equal(
        actual,
        expected,
        'pois(2, 3) should return expected PMF value',
        abs_tol=1e-12,
    )


@pytest.mark.parametrize('x,mean,expected_error', [
    ('2', 3, InvalidTypeError),
    (2, float('inf'), ProhibitedValueError),
    (2, float('nan'), ProhibitedValueError),
    (2, 0, ValueBelowBoundsError),
    (2, -1, ValueBelowBoundsError),
])
def test_pois_invalid_inputs(x, mean, expected_error):
    '''Test pois raises expected errors for invalid count/mean inputs.'''
    assert_raises_expected(
        lambda: pois(x, mean),
        expected_error,
        f'pois should raise {expected_error.__name__} for inputs ({x}, {mean})',
    )


def test_pois_exponent_overflow_guard():
    '''Test pois raises ValueAboveBoundsError when mean**x exceeds validator safety bound.'''
    assert_raises_expected(
        lambda: pois(20, 10),
        ValueAboveBoundsError,
        'pois should raise ValueAboveBoundsError for unsafe exponentiation input',
    )
        
        