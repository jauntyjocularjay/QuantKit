# For package usage
try: 
    from ..pytilities import console 
# For direct script usage
except ImportError:
    from ..pytilities import console as console
import statistics as Statistics
from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import Literal, Union
from pprint import pprint
from ..pytilities.validation import *
from ..pytilities.returns import *

def median_index(data_list: Sequence):
    ''' Returns the index or indices of the median value(s) in a sorted version of the input list.

    - For an odd-length list, returns a single-element tuple containing the index of the median.
    - For an even-length list, returns a tuple containing the indices of the two middle values.

    Parameters:
        data_list (list, optional): The input list of values. Defaults to None.

    Returns:
        tuple: Indices of the median value(s) in the sorted list. Returns an empty tuple if the input 
          is None or empty.

    Examples:
        median_index([1, 2, 3, 4, 5, 6, 7])  # returns (3,)
        median_index([1, 2, 3, 4, 5, 6])     # returns (2, 3)
    '''

    if data_list is None:
        return ()
    if not sequence_are_numbers(data_list):
        raise NotNumericSequenceError
    if len(data_list) == 0:
        return ()
    
    data_list = sorted(data_list)

    # if the data_list length is odd
    if(len(data_list) % 2 == 1): 
        return ( len(data_list) // 2, )

    # if the data_list length is even
    else:
        lower_index = len(data_list) // 2 - 1
        higher_index = len(data_list) // 2
        return (lower_index, higher_index)

def interquartile_slice(data_list: Sequence):
    ''' Returns the data points within the interquartile range (IQR) of the input list using 
    index-based slicing.

    - This function sorts the input data and returns a slice containing the 'middle 50%' of 
    values, i.e., those between the lower and upper quartiles, using integer indices (no 
    interpolation).
    - This is not the standard IQR value (Q3 - Q1), but rather the actual data points that fall 
    within the IQR range. 

    Parameters:
        data_list (Sequence): The input list of numeric values. Defaults to None.

    Returns:
        list, set, or tuple: A slice of the sorted data representing the interquartile range,
        or None if the input is None or empty.

    Example:
        iqr_slice([1, 2, 3, 4, 5, 6, 7, 8, 9])  # returns [3, 4, 5, 6, 7]
    '''

    if data_list is None:
        return None
    elif not sequence_are_numbers(data_list):
        raise TypeError(f'All elements in {data_list} must be numbers')
    elif len(data_list) <= 0:
        return None

    input_type = type(data_list)
    data_list = sorted(data_list)

    if(len(data_list) % 2 == 1):
        iqr_length = (len(data_list) + 1) // 2
    else:
        iqr_length = len(data_list) // 2

    initial_index = iqr_length // 2
    result = data_list[initial_index:initial_index+iqr_length]

    return original_sequence_type(input_type, result)

def iqs(data_list: Sequence):
    return interquartile_slice(data_list)


# Classes
