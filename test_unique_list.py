import pytest
from quantkit.unique_list import unique_list
from pytilities.validation import DuplicateValueError

# --- __setitem__ tests ---
def test_setitem_single_value():
    '''Test: __setitem__ sets a unique value at an index.'''
    ls = unique_list(1, 2, 3)
    ls[0] = 4
    assert ls[0] == 4, '__setitem__ should update the value at index 0'
    assert 4 in ls.lookup_set, 'lookup_set should include the new value'
    assert 1 not in ls.lookup_set, 'lookup_set should not include the replaced value'


def test_setitem_duplicate_raises():
    '''Test: __setitem__ raises DuplicateValueError for duplicate value.'''
    ls = unique_list(1, 2, 3)
    with pytest.raises(DuplicateValueError):
        ls[0] = 2  # 2 already exists


def test_setitem_slice_unique():
    '''Test: __setitem__ with slice sets unique values.'''
    ls = unique_list(1, 2, 3, 4)
    ls[1:3] = [5, 6]
    assert ls[1] == 5 and ls[2] == 6, '__setitem__ should update values in slice'
    assert 5 in ls.lookup_set and 6 in ls.lookup_set, 'lookup_set should include new values'
    assert 2 not in ls.lookup_set and 3 not in ls.lookup_set, 'lookup_set should not include replaced values'


def test_setitem_slice_duplicate_raises():
    '''Test: __setitem__ with slice raises DuplicateValueError for duplicate.'''
    ls = unique_list(1, 2, 3, 4)
    with pytest.raises(DuplicateValueError):
        ls[1:3] = [2, 5]  # 2 already exists
