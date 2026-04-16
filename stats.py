import math as Math
import statistics as Statistics
import console
from collections.abc import Sequence
from typing import Literal

# To import use from the same folder:
# import stats 
#
# To import use from the parent folder:
# from PyTils import stats 

console.clear()

def median_index(data_list: Sequence):
	""" Returns the index or indices of the median value(s) in a sorted version of the input list.

	For an odd-length list, returns a single-element tuple containing the index of the median.
	For an even-length list, returns a tuple containing the indices of the two middle values.

	Parameters:
		data_list (list, optional): The input list of values. Defaults to None.

	Returns:
		tuple: Indices of the median value(s) in the sorted list. Returns an empty tuple if the input is None or empty.

	Examples:
		median_index([1, 2, 3, 4, 5, 6, 7])  # returns (3,)
		median_index([1, 2, 3, 4, 5, 6])	 # returns (2, 3)
	"""

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
	""" Returns the data points within the interquartile range (IQR) of the input list using 
	index-based slicing.

	This function sorts the input data and returns a slice containing the "middle 50%" of 
	values, i.e., those between the lower and upper quartiles, using integer indices (no 
	interpolation).
	This is not the standard IQR value (Q3 - Q1), but rather the actual data points that fall 
	within the IQR range. 

	Parameters:
		data_list (Sequence): The input list of numeric values. Defaults to None.

	Returns:
		list, set, or tuple: A slice of the sorted data representing the interquartile range,
		or None if the input is None or empty.

	Example:
		iqr_slice([1, 2, 3, 4, 5, 6, 7, 8, 9])  # returns [3, 4, 5, 6, 7]
	"""

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

	return basic_sequence(input_type, result)

def iqs(data_list: Sequence):
	return interquartile_slice(data_list)

def box_plotify(data_list: Sequence, quantile_method: Literal['exclusive', 'inclusive'] = 'exclusive'):
	"""Calculate box plot parameters (min, Q1, median, Q3, max) for a numeric sequence.

	This function computes the five-number summary required for a box plot: minimum, first quartile (Q1),
	median (Q2), third quartile (Q3), and maximum. Quartiles are calculated using the specified method.

	Parameters:
		data_list (Sequence): A sequence of numeric values (length >= 4).
		quantile_method (Literal['exclusive', 'inclusive']): Method for quartile calculation. Defaults to 'exclusive'.

	Returns:
		dict: A dictionary with keys 'min', 'q1', 'median', 'q3', and 'max'.

	Raises:
		InvalidSequenceError: If data_list is not a valid sequence.
		NotNumericSequenceError: If data_list contains non-numeric values.
		ValueError: If data_list has fewer than 4 elements.

	Example:
		box_plot_params([1, 2, 3, 4, 5, 6])
		# returns {'min': 1, 'q1': 2.25, 'median': 3.5, 'q3': 4.75, 'max': 6}
	"""
	if data_list is None or not isinstance(data_list, Sequence):
		raise InvalidSequenceError
	if not sequence_are_numbers(data_list):
		raise NotNumericSequenceError
	if len(data_list) < 4:
		raise ValueError('argument must have at least length 4')

	data_list = sorted(data_list)
	quartiles = Statistics.quantiles(data_list, n=4, method = quantile_method)

	return {
		'min': data_list[0],
		'q1': quartiles[0],
		'median': Statistics.median(data_list), # aka 'q2'
		'q3': quartiles[2],
		'max': data_list[-1]
	}

# Errors
class InvalidSequenceError(TypeError):
	"""Exception raised when an argument is not a valid sequence.

	Raised by statistical functions when the input is not a sequence type (e.g., list, tuple, set).

	Example:
		if not isinstance(data_list, Sequence):
			raise InvalidSequenceError
	"""
	def __init__(self, message=f"expected a {Sequence}"):
		super().__init__(message)

class NotNumericSequenceError(TypeError):
	"""Exception raised when a sequence contains non-numeric elements.

	Raised by statistical functions when the input sequence contains elements that are not real numbers.

	Example:
		if not sequence_are_numbers(data_list):
			raise NotNumericSequenceError
	"""
	def __init__(self, message=f"expected a {Sequence} real numbers"):
		super().__init__(message)

# Helpers
def sequence_are_numbers(data_list: Sequence):
	""" Checks that all elements in data_list are numeric (int or float), or that data_list is None.

	This function is intended to validate input for statistical analysis functions. If any element
	in the list is not an integer or float.

	Parameters:
		data_list (list or None): The input list to check.

	Raises:
		TypeError: If any element in data_list is not an int or float.

	Example:
		sequence_are_numbers([1, 2.5, 3])	# returns True
		sequence_are_numbers(['a', 2, 3])	# returns false
		sequence_are_numbers(None)			# raises TypeError
	"""
	if not isinstance(data_list, Sequence):
		raise InvalidSequenceError

	for x in data_list:
		if not isinstance(x, (int, float)) or Math.isnan(x) or Math.isinf(x):
			return False

	return True

def basic_sequence(input_type, data_list):
	"""Return a sequence of the same type as input_type, populated with data_list's elements.

	Converts the provided data_list into a set, tuple, or list, matching the type of input_type.
	If input_type is set, returns a set; if tuple, returns a tuple; otherwise, returns a list.

	Parameters:
		input_type: The type to match (set, tuple, or list).
		data_list: The data to convert.

	Returns:
		A new sequence (set, tuple, or list) containing the elements of data_list.

	Example:
		basic_sequence(list, [1, 2, 3])   # returns [1, 2, 3]
		basic_sequence(tuple, [1, 2, 3])  # returns (1, 2, 3)
		basic_sequence(set, [1, 2, 3])    # returns {1, 2, 3}
	"""
	if input_type is set:
		return set(data_list)
	elif input_type is tuple:
		return tuple(data_list)
	else:
		return list(data_list)








