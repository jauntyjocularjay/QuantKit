
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import PyTils.stats as stats
import pytest
from typing import Literal

# Shared constants for DRYness
EXPECTED_BOXPLOT_KEYS = [
    stats.SEQUENCE_MINIMUM, stats.Q1, stats.SEQUENCE_MEDIAN, stats.Q2, stats.Q3,
    stats.SEQUENCE_MAXIMUM, stats.TUKEY_FENCE, stats.DATA_LIST, stats.OUTLIERS, stats.IQR, stats.SEQUENCE_RANGE
]

# --- median_index tests ---
import math

@pytest.mark.parametrize(
    "input_list,expected,desc",
    [
        ([1, 2, 3, 4, 5], (2,), "sorted odd-length list"),
        ([5, 4, 3, 2, 1], (2,), "unsorted odd-length list"),
        ([10], (0,), "single-element list"),
        ([1, 2, 3, 4, 5, 6], (2, 3), "sorted even-length list"),
        ([6, 5, 4, 3, 2, 1], (2, 3), "unsorted even-length list"),
        ([10, 20], (0, 1), "two-element list"),
        ([], (), "empty list"),
        (None, (), "None input"),
        ([1, 2, 2, 3, 4], (2,), "odd-length list with duplicates"),
        ([1, 2, 2, 3, 4, 4], (2, 3), "even-length list with duplicates"),
    ]
)
def test_median_index(input_list, expected, desc):
    """Test median_index for various cases: odd/even, sorted/unsorted, duplicates, empty, None."""
    result = stats.median_index(input_list)
    assert result == expected, f"median_index should return {expected} for {desc}, got {result}"


# --- iqr_slice tests ---
@pytest.mark.parametrize(
    "input_list,expected,desc",
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], [3, 4, 5, 6, 7], "odd-length list"),
        ([1, 2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6], "even-length list"),
    ]
)
def test_iqr_slice_typical(input_list, expected, desc):
    """Test interquartile_slice returns correct slice for typical odd/even-length lists."""
    result = stats.interquartile_slice(input_list)
    assert result == expected, f"iqr_slice should return {expected} for {desc}, got {result}"

@pytest.mark.parametrize("input_list,desc", [([], "empty list"), (None, "None input")])
def test_iqr_slice_empty_none(input_list, desc):
    """Test interquartile_slice returns None for empty or None input."""
    result = stats.interquartile_slice(input_list)
    assert result is None, f"iqr_slice should return None for {desc}, got {result}"

def test_iqr_slice_non_numeric():
    """Test interquartile_slice raises TypeError for non-numeric input."""
    with pytest.raises(TypeError):
        stats.interquartile_slice([1, 'a', 3])


# --- iqs tests ---
def test_iqs_equivalence():
    """Test that iqs returns the same result as interquartile_slice for the same input."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = stats.iqs(data)
    expected = stats.interquartile_slice(data)
    assert result == expected, "iqs should return the same result as interquartile_slice for the same input"


# --- box_plotify tests ---
def test_box_plotify_typical():
    """Test box_plotify returns correct keys and values for a typical list."""
    data = [1, 2, 3, 4, 5, 6]
    result = stats.box_plotify(data)
    for key in ['min', 'q1', 'median', 'q3', 'max']:
        assert key in result, f"box_plotify result should contain key '{key}'"

def test_box_plotify_inclusive():
    """Test box_plotify with inclusive quantile method returns a dictionary."""
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    result = stats.box_plotify(data, quantile_method='inclusive')
    assert isinstance(result, dict), "box_plotify should return a dictionary for valid input"

def test_box_plotify_invalid_sequence():
    """Test box_plotify raises NotNumericSequenceError for a sequence of non-numeric elements (e.g., a string)."""
    with pytest.raises(stats.NotNumericSequenceError, match="expected"):
        stats.box_plotify('1234')

def test_box_plotify_not_numeric():
    """Test box_plotify raises NotNumericSequenceError for non-numeric sequence."""
    with pytest.raises(stats.NotNumericSequenceError, match="real numbers"):
        stats.box_plotify([1, 'a', 3, 4])

def test_box_plotify_too_short():
    """Test box_plotify raises ValueError for sequence shorter than 4 elements."""
    with pytest.raises(ValueError, match="at least length 4"):
        stats.box_plotify([1, 2, 3])


# --- Error class tests ---
def test_invalid_sequence_error():
    """Test InvalidSequenceError can be raised and has correct message."""
    with pytest.raises(stats.InvalidSequenceError, match="expected"):
        raise stats.InvalidSequenceError()

def test_not_numeric_sequence_error():
    """Test NotNumericSequenceError can be raised and has correct message."""
    with pytest.raises(stats.NotNumericSequenceError, match="real numbers"):
        raise stats.NotNumericSequenceError()


# --- sequence_are_numbers tests ---
def test_sequence_are_numbers_all_numeric():
    """Test sequence_are_numbers returns True for all-numeric sequence."""
    assert stats.sequence_are_numbers([1, 2.5, 3]), "sequence_are_numbers should return True for all numeric sequence"

def test_sequence_are_numbers_non_numeric():
    """Test sequence_are_numbers returns False if any element is not numeric."""
    assert not stats.sequence_are_numbers([1, 'a', 3]), "sequence_are_numbers should return False if any element is not numeric"

def test_sequence_are_numbers_nan_inf():
    """Test sequence_are_numbers returns False if any element is NaN or infinite."""
    assert not stats.sequence_are_numbers([1, float('nan'), 3]), "sequence_are_numbers should return False if any element is NaN"
    assert not stats.sequence_are_numbers([1, float('inf'), 3]), "sequence_are_numbers should return False if any element is infinite"

# --- basic_sequence tests ---
def test_basic_sequence_list():
    """Test basic_sequence returns a list if input_type is list."""
    result = stats.basic_sequence(list, [1, 2, 3])
    assert isinstance(result, list), "basic_sequence should return a list if input_type is list"
    assert result == [1, 2, 3], "basic_sequence should preserve elements for list input"

def test_basic_sequence_tuple():
    """Test basic_sequence returns a tuple if input_type is tuple."""
    result = stats.basic_sequence(tuple, [1, 2, 3])
    assert isinstance(result, tuple), "basic_sequence should return a tuple if input_type is tuple"
    assert result == (1, 2, 3), "basic_sequence should preserve elements for tuple input"

def test_basic_sequence_set():
    """Test basic_sequence returns a set if input_type is set."""
    result = stats.basic_sequence(set, [1, 2, 3])
    assert isinstance(result, set), "basic_sequence should return a set if input_type is set"
    assert set(result) == {1, 2, 3}, "basic_sequence should preserve elements for set input"

# --- Additional coverage tests ---
def test_median_index_not_numeric():
    """Test median_index raises NotNumericSequenceError for non-numeric input."""
    with pytest.raises(stats.NotNumericSequenceError):
        stats.median_index(['a', 2, 3])

def test_box_plotify_none():
    """Test box_plotify raises InvalidSequenceError for None input."""
    with pytest.raises(stats.InvalidSequenceError):
        stats.box_plotify(None)

def test_sequence_are_numbers_none():
    """Test sequence_are_numbers raises InvalidSequenceError for None input."""
    with pytest.raises(stats.InvalidSequenceError):
        stats.sequence_are_numbers(None)


# --- BoxPlot class tests ---
def test_boxplot_as_dict_and_str():
    """Test BoxPlot.as_dict() and __str__() for correct output and keys."""
    """Test BoxPlot.as_dict() returns all expected keys."""
    data = [1, 2, 3, 4, 5, 6]
    bp = stats.BoxPlot(data)
    d = bp.as_dict()
    for key in EXPECTED_BOXPLOT_KEYS:
        assert key in d, f"BoxPlot.as_dict() should contain key '{key}'"

def test_boxplot_str_and_min_max():
    """Test BoxPlot __str__ output and min/max whisker logic."""
    data = [1, 2, 3, 4, 5, 6]
    bp = stats.BoxPlot(data)
    s = str(bp)
    assert str(bp.q1) in s, "BoxPlot.__str__ should include q1 value"
    assert str(bp.median) in s, "BoxPlot.__str__ should include median value"
    assert str(bp.q3) in s, "BoxPlot.__str__ should include q3 value"
    tukey = bp.tukey_fence
    min_val = next((x for x in bp.data_list if x >= tukey[stats.SEQUENCE_MINIMUM]), bp.data_list[0])
    max_val = next((x for x in reversed(bp.data_list) if x <= tukey[stats.SEQUENCE_MAXIMUM]), bp.data_list[-1])
    assert bp.min == min_val, "BoxPlot.min should match Tukey whisker logic or fallback to first value"
    assert bp.max == max_val, "BoxPlot.max should match Tukey whisker logic or fallback to last value"

def test_boxplot_properties():
    """Test BoxPlot properties: range, iqr, iqr_balance, whisker_balance."""
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    """Test BoxPlot range, IQR, iqr_balance, whisker_balance, and outliers properties."""
    bp = stats.BoxPlot(data)
    assert bp.range == bp.max - bp.min, "BoxPlot.range should be max - min"
    assert bp.iqr == bp.q3 - bp.q1, "BoxPlot.iqr should be q3 - q1"
    left = bp.median - bp.q1
    right = bp.q3 - bp.median
    expected_balance = (left - right) / bp.iqr
    assert abs(bp.iqr_balance - expected_balance) < 1e-9, "BoxPlot.iqr_balance should match formula"
    left_w = bp.q1 - bp.min
    right_w = bp.max - bp.q3
    expected_wb = (left_w - right_w) / bp.range
    assert abs(bp.whisker_balance - expected_wb) < 1e-9, "BoxPlot.whisker_balance should match formula"
    outliers = [x for x in bp.data_list if x < bp.tukey_fence[stats.SEQUENCE_MINIMUM] or x > bp.tukey_fence[stats.SEQUENCE_MAXIMUM]]
    assert bp.outliers == outliers, "BoxPlot.outliers should match Tukey fence logic"

def test_boxplot_invalid_sequence():
    """Test BoxPlot raises InvalidSequenceError for non-sequence input."""
    with pytest.raises(stats.InvalidSequenceError):
        stats.BoxPlot(None)

def test_boxplot_not_numeric():
    """Test BoxPlot raises NotNumericSequenceError for non-numeric sequence."""
    with pytest.raises(stats.NotNumericSequenceError):
        stats.BoxPlot([1, 'a', 3, 4])

def test_boxplot_too_short():
    """Test BoxPlot raises ValueError for sequence shorter than 4 elements."""
    with pytest.raises(ValueError):
        stats.BoxPlot([1, 2, 3])

def test_boxplot_inclusive_method():
    """Test BoxPlot with inclusive quantile method."""
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    bp = stats.BoxPlot(data, quantile_method='inclusive')
    assert isinstance(bp, stats.BoxPlot), "BoxPlot should be created with inclusive method"


