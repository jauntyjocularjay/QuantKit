
import pytest
import stats
import console
from typing import Literal


console.clear()

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
    # Test median_index for various cases
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
    # Test iqr_slice for typical cases
    result = stats.interquartile_slice(input_list)
    assert result == expected, f"iqr_slice should return {expected} for {desc}, got {result}"

@pytest.mark.parametrize("input_list,desc", [([], "empty list"), (None, "None input")])
def test_iqr_slice_empty_none(input_list, desc):
    # Test iqr_slice returns None for empty or None input
    result = stats.interquartile_slice(input_list)
    assert result is None, f"iqr_slice should return None for {desc}, got {result}"

def test_iqr_slice_non_numeric():
    # Test iqr_slice raises TypeError for non-numeric input
    with pytest.raises(TypeError):
        stats.interquartile_slice([1, 'a', 3])


# --- iqs tests ---
def test_iqs_equivalence():
    # Test that iqs returns the same as interquartile_slice
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = stats.iqs(data)
    expected = stats.interquartile_slice(data)
    assert result == expected, "iqs should return the same result as interquartile_slice for the same input"


# --- box_plotify tests ---
def test_box_plotify_typical():
    # Test box_plotify returns correct keys and types for a typical list
    data = [1, 2, 3, 4, 5, 6]
    result = stats.box_plotify(data)
    for key in ['min', 'q1', 'median', 'q3', 'max']:
        assert key in result, f"box_plotify result should contain key '{key}'"
    assert result['min'] == 1, "box_plotify should return correct minimum value"
    assert result['max'] == 6, "box_plotify should return correct maximum value"

def test_box_plotify_inclusive():
    # Test box_plotify with inclusive quantile method
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    result = stats.box_plotify(data, quantile_method='inclusive')
    assert isinstance(result, dict), "box_plotify should return a dictionary for valid input"

def test_box_plotify_invalid_sequence():
    # Test box_plotify raises NotNumericSequenceError for a sequence of non-numeric elements (e.g., a string)
    with pytest.raises(stats.NotNumericSequenceError, match="expected"):
        stats.box_plotify('1234')

def test_box_plotify_not_numeric():
    # Test box_plotify raises NotNumericSequenceError for non-numeric sequence
    with pytest.raises(stats.NotNumericSequenceError, match="real numbers"):
        stats.box_plotify([1, 'a', 3, 4])

def test_box_plotify_too_short():
    # Test box_plotify raises ValueError for short sequence
    with pytest.raises(ValueError, match="at least length 4"):
        stats.box_plotify([1, 2, 3])


# --- Error class tests ---
def test_invalid_sequence_error():
    # Test InvalidSequenceError can be raised and has correct message
    with pytest.raises(stats.InvalidSequenceError, match="expected"):
        raise stats.InvalidSequenceError()

def test_not_numeric_sequence_error():
    # Test NotNumericSequenceError can be raised and has correct message
    with pytest.raises(stats.NotNumericSequenceError, match="real numbers"):
        raise stats.NotNumericSequenceError()


# --- sequence_are_numbers tests ---
def test_sequence_are_numbers_all_numeric():
    # Test sequence_are_numbers returns True for all numeric sequence
    assert stats.sequence_are_numbers([1, 2.5, 3]), "sequence_are_numbers should return True for all numeric sequence"

def test_sequence_are_numbers_non_numeric():
    # Test sequence_are_numbers returns False for sequence with non-numeric
    assert not stats.sequence_are_numbers([1, 'a', 3]), "sequence_are_numbers should return False if any element is not numeric"

def test_sequence_are_numbers_nan_inf():
    # Test sequence_are_numbers returns False for sequence with nan or inf
    assert not stats.sequence_are_numbers([1, float('nan'), 3]), "sequence_are_numbers should return False if any element is NaN"
    assert not stats.sequence_are_numbers([1, float('inf'), 3]), "sequence_are_numbers should return False if any element is infinite"

# --- basic_sequence tests ---
def test_basic_sequence_list():
    # Test basic_sequence returns a list for list input_type
    result = stats.basic_sequence(list, [1, 2, 3])
    assert isinstance(result, list), "basic_sequence should return a list if input_type is list"
    assert result == [1, 2, 3], "basic_sequence should preserve elements for list input"

def test_basic_sequence_tuple():
    # Test basic_sequence returns a tuple for tuple input_type
    result = stats.basic_sequence(tuple, [1, 2, 3])
    assert isinstance(result, tuple), "basic_sequence should return a tuple if input_type is tuple"
    assert result == (1, 2, 3), "basic_sequence should preserve elements for tuple input"

def test_basic_sequence_set():
    # Test basic_sequence returns a set for set input_type
    result = stats.basic_sequence(set, [1, 2, 3])
    assert isinstance(result, set), "basic_sequence should return a set if input_type is set"
    assert set(result) == {1, 2, 3}, "basic_sequence should preserve elements for set input"


