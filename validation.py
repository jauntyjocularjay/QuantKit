import math as Math
from collections.abc import Sequence

def sequence_are_numbers(data_list: Sequence):
    """ Checks that all elements in data_list are numeric (int or float), or that data_list is None.

    This function is intended to validate input for statistical analysis functions. If any element
    in the list is not an integer or float.

    Parameters:
        data_list (list or None): The input list to check.

    Raises:
        TypeError: If any element in data_list is not an int or float.

    Example:
        sequence_are_numbers([1, 2.5, 3])    # returns True
        sequence_are_numbers(['a', 2, 3])    # returns false
        sequence_are_numbers(None)            # raises TypeError
    """
    if not isinstance(data_list, Sequence) or isinstance(data_list, (str,bytes)):
        raise InvalidSequenceError

    for x in data_list:
        if not isinstance(x, (int, float)) or Math.isnan(x) or Math.isinf(x) or isinstance(x, bool):
            return False

    return True

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
