import pytest
from pytils.returns import original_sequence_type
from pytils.validation import InvalidSequenceError, NotNumericSequenceError
from collections import deque, UserList
from array import array as Array

# --- List, Tuple, Set ---
def test_return_list():
    """Should return a list when input_type is list."""
    result = original_sequence_type(list, (1, 2, 3))
    assert isinstance(result, list), "Should return a list for list input_type"
    assert result == [1, 2, 3], "Should preserve elements for list input_type"

def test_return_tuple():
    """Should return a tuple when input_type is tuple."""
    result = original_sequence_type(tuple, [1, 2, 3])
    assert isinstance(result, tuple), "Should return a tuple for tuple input_type"
    assert result == (1, 2, 3), "Should preserve elements for tuple input_type"

def test_return_set():
    """Should return a set when input_type is set."""
    result = original_sequence_type(set, [1, 2, 3, 2])
    assert isinstance(result, set), "Should return a set for set input_type"
    assert set(result) == {1, 2, 3}, "Should preserve unique elements for set input_type"

# --- String, Bytes, Bytearray ---
def test_return_str():
    """Should return a string when input_type is str."""
    result = original_sequence_type(str, ['a', 'b', 'c'])
    assert isinstance(result, str), "Should return a string for str input_type"
    assert result == "['a', 'b', 'c']", "Should match string representation"

def test_return_bytes():
    """Should return bytes when input_type is bytes."""
    result = original_sequence_type(bytes, [65, 66, 67])
    assert isinstance(result, bytes), "Should return bytes for bytes input_type"
    assert result == b'ABC', "Should match bytes representation for ASCII values"

def test_return_bytearray():
    """Should return bytearray when input_type is bytearray."""
    result = original_sequence_type(bytearray, [65, 66, 67])
    assert isinstance(result, bytearray), "Should return bytearray for bytearray input_type"
    assert result == bytearray(b'ABC'), "Should match bytearray representation for ASCII values"

# --- Range ---
def test_return_range():
    """Should return a range when input_type is range and input is numeric."""
    result = original_sequence_type(range, [1, 2, 3, 4, 5])
    assert isinstance(result, range), "Should return a range for range input_type"
    assert list(result) == list(range(1, 5)), "Should match range from min to max"

# --- Deque ---
def test_return_deque():
    """Should return a deque when input_type is deque."""
    result = original_sequence_type(deque, [1, 2, 3])
    assert isinstance(result, deque), "Should return a deque for deque input_type"
    assert list(result) == [1, 2, 3], "Should preserve elements for deque input_type"

# --- Array ---
def test_return_array():
    """Should return an array when input_type is Array."""
    result = original_sequence_type(Array, [1, 2, 3])
    assert isinstance(result, Array), "Should return an array for Array input_type"
    assert list(result) == [1, 2, 3], "Should preserve elements for Array input_type"

# --- UserList ---
def test_return_userlist():
    """Should return a UserList when input_type is UserList."""
    result = original_sequence_type(UserList, [1, 2, 3])
    assert isinstance(result, UserList), "Should return a UserList for UserList input_type"
    assert list(result) == [1, 2, 3], "Should preserve elements for UserList input_type"

# --- Error Cases ---
def test_non_sequence_input():
    """Should raise TypeError if data_list is not a Sequence."""
    with pytest.raises(TypeError):
        original_sequence_type(list, 123)

# --- Additional coverage tests ---
def test_range_non_numeric():
    """Should not return range if input is not all numeric."""
    result = original_sequence_type(range, ['a', 'b', 'c'])
    # Should fall through and return None
    assert result is None, "Should return None for non-numeric range input"

def test_range_empty():
    """Should not fail for empty input with range type."""
    result = original_sequence_type(range, [])
    assert isinstance(result, range) and list(result) == list(range(0)), "Should return range(0) for empty input with range type"

def test_range_single_element():
    """Should return a degenerate range for single numeric input."""
    result = original_sequence_type(range, [5])
    assert isinstance(result, range), "Should return a range for single numeric input"
    assert list(result) == [], "Degenerate range should be empty (start==stop)"

def test_fallthrough_branch():
    """Should return None if input_type is not handled."""
    class Dummy: pass
    result = original_sequence_type(Dummy, [1, 2, 3])
    assert result is None, "Should return None for unhandled input_type"
