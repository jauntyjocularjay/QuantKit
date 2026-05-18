# For package usage
import statistics as Statistics
import math as Math
from collections.abc import Sequence
from typing import Literal, Union
from fractions import Fraction
from .constants import *
from .pytilities.validation import *
from .pytilities.returns import *

def median_index(data_list: Sequence):
    ''' Returns the index or indices of the median value(s) in a sorted version of the input list.

    - For an odd-length list, returns a single-element tuple containing the index of the median.
    - For an even-length list, returns a tuple containing the indices of the two middle values.

    Parameters:
        data_list (Sequence): The input sequence of numeric values.

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
        data_list (Sequence): The input sequence of numeric values.

    Returns:
        list, set, or tuple: A slice of the sorted data representing the interquartile range,
        or None if the input is None or empty.

    Example:
        interquartile_slice([1, 2, 3, 4, 5, 6, 7, 8, 9])  # returns [3, 4, 5, 6, 7]
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
    """Alias for `interquartile_slice`. Returns the data points within the IQR of the input list."""
    return interquartile_slice(data_list)

def binom(p: Union[Fraction, int, float], n_trials: int = 1, k_success: int = 1):
    """Calculate binomial distribution statistics for a given probability of success.

    Computes the probability, binomial coefficient, mean, and standard deviation for
    the binomial distribution with probability of success `p`, `n_trials` total trials,
    and `k_success` desired successes.

    Parameters
    ----------
    p : Fraction | int | float
        Probability of success on a single trial (0 < p < 1).
    n_trials : int, optional
        Total number of trials. Must be greater than `k_success`. Defaults to 1.
    k_success : int, optional
        Number of desired successes. Defaults to 1.

    Returns
    -------
    dict
        Dictionary with keys VALUE, COEF, MEAN, and SDEV:
        - VALUE: Probability of exactly k_success successes in n_trials trials.
        - COEF: Binomial coefficient C(n_trials, k_success).
        - MEAN: Expected number of successes (n * p).
        - SDEV: Standard deviation as both a symbolic string and a float.

    Raises
    ------
    TypeError, ValueError
        If input parameters are invalid or out of range.
    """
    validate_as(p, (Fraction, int, float))
    if isinstance (p, float): validate_float(p)
    validate_is_greater_than(p, 0)
    validate_is_less_than(p,1)
    validate_is_greater_or_equal_to(n_trials, k_success)
    validate_against(n_trials, (0,))
    validate_against(p, (0, 1))

    p = Fraction(p)
    q = Fraction(p.denominator - p.numerator, p.denominator)
    coefficient = nck(n_trials, k_success)

    product_of_success = p ** k_success
    product_of_failure = q ** (n_trials - k_success)

    return {
        VALUE: coefficient * product_of_success * product_of_failure,
        COEF: coefficient,
        MEAN: n_trials * p,
        STD_DEV: {
            FRAC: f'sqrt({n_trials * p * q})',
            FLOAT: Math.sqrt(n_trials * p * q)
        }
    }

def nck(n_trials: int, k_success: int):
    validate_as(n_trials, int)
    validate_as(k_success, int)
    validate_is_greater_or_equal_to(n_trials, k_success)
    
    return Fraction(Math.factorial(n_trials), Math.factorial(k_success) * Math.factorial(n_trials - k_success))

def geom(p: Union[Fraction, int, float], k_trials: int = 1, includes_success: bool = True):
    """ Calculate geometric distribution statistics for a given probability of success.

    Computes the probability, mean, and standard deviation for the geometric distribution
    with probability of success `p` and number of trials `k_trials`. The function supports
    both definitions: counting the trial on which the first success occurs (`includes_success=True`)
    or the number of failures before the first success (`includes_success=False`).

    Parameters
    ----------
    p : Fraction | int | float
        Probability of success on a single trial (0 < p < 1).
    k_trials : int, optional
        The trial number (if includes_success=True) or number of failures (if includes_success=False).
        Defaults to 1 (first trial).
    includes_success : bool, optional
        If True, k_trials counts the trial of first success (default). If False, counts failures before success.

    Returns
    -------
    dict
        Dictionary with keys VALUE, MEAN, and SDEV:
        - VALUE: Probability of first success at k_trials as a Fraction.
        - MEAN: Expected value as a Fraction.
        - SDEV: Standard deviation as both a symbolic string (FRAC) and a float (FLOAT).

    Raises
    ------
    TypeError, ValueError
        If input parameters are invalid or out of range.
    """
    validate_as(p, (Fraction, int, float))
    if isinstance (p, float): validate_float(p)
    validate_is_greater_than(p, 0)
    validate_is_less_than(p, 1)
    validate_against(p, (0, 1))

    p = Fraction(p)
    q = Fraction(p.denominator - p.numerator, p.denominator)
    value = p * pow(q,k_trials - 1) if includes_success else p * pow(q, k_trials)
    mean = Fraction(p.denominator, p.numerator) if includes_success else Fraction(1-p, p)
    variance = Fraction(q, p**2) 

    return {
        VALUE: value,
        MEAN: mean,
        STD_DEV: {
            FRAC_STR: f'math.sqrt(Fraction({variance}))',
            FLOAT: float(Math.sqrt(variance))
        }
    }

def geoh(pop_i: int, pop_b: int, n_trials:int, k_success: int):
    ''' Hyperbolic-Geomtric Distribution Function
    pop_i = the population of interest
    pop_b = the rest of the population
    n_trials = the number of trials
    k_success = the target number of successes
    '''

    validate_as(n_trials, int)
    validate_as(k_success, int)
    validate_is_greater_or_equal_to(n_trials, k_success)
    validate_is_greater_than(pop_i, 0)
    validate_is_greater_than(pop_b, 0)
    validate_is_greater_than(n_trials, 0)
    validate_is_greater_than(k_success, 0)

    r = nck(pop_i, k_success)
    bnk = nck(pop_b, n_trials - k_success)
    rbn = nck(pop_i + pop_b, n_trials)

    return Fraction(r * bnk / rbn)
