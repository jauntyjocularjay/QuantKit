import statistics as Statistics

# To import use from the same folder:
# import stats 
#
# To import use from the parent folder:
# from PyTils import stats 

def median_index(data_list: list = None):
    """
    Returns the index or indices of the median value(s) in a sorted version of the input list.

    For an odd-length list, returns a single-element tuple containing the index of the median.
    For an even-length list, returns a tuple containing the indices of the two middle values.

    Parameters:
        data_list (list, optional): The input list of values. Defaults to None.

    Returns:
        tuple: Indices of the median value(s) in the sorted list. Returns an empty tuple if the input is None or empty.

    Examples:
        median_index([1, 2, 3, 4, 5, 6, 7])  # returns (3,)
        median_index([1, 2, 3, 4, 5, 6])     # returns (2, 3)
    """
    # if void or an empty data_list is passed

    check_list_items_are_numbers(data_list)

    if(data_list is None or len(data_list) == 0):
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

def iqr_slice(data_list: list = None):
    """ Returns the data points within the interquartile range (IQR) of the input list using 
    index-based slicing.

    This function sorts the input data and returns a slice containing the "middle 50%" of 
    values, i.e., those between the lower and upper quartiles, using integer indices (no 
    interpolation).
    This is not the standard IQR value (Q3 - Q1), but rather the actual data points that fall 
    within the IQR range. Useful for exploratory data analysis and visualizations where you 
    want to examine or plot the spread of the central data.

    Parameters:
        data_list (list, optional): The input list of numeric values. Defaults to None.

    Returns:
        list or None: A slice of the sorted data representing the interquartile range,
        or None if the input is None or empty.

    Example:
        iqr_slice([1, 2, 3, 4, 5, 6, 7, 8, 9])  # returns [3, 4, 5, 6, 7]
    """

    check_list_items_are_numbers(data_list)

    if(data_list is None or len(data_list) < 0):
        return None

    data_list = sorted(data_list)

    if(len(data_list) % 2 == 1):
        data = data_list[:Statistics.median(data_list)-1] + data_list[Statistics.median(data_list):]

    lower_bound = Statistics.median_low(data)-1
    higher_bound = Statistics.median_high(data)

    return data_list[lower_bound:higher_bound]

# Helpers
# Error checking
def check_list_items_are_numbers(data_list: list):
    """ Checks that all elements in data_list are numeric (int or float), or that data_list is None.

    This function is intended to validate input for statistical analysis functions. If any element
    in the list is not an integer or float, a TypeError is raised. If data_list is None, the check
    passes silently.

    Parameters:
        data_list (list or None): The input list to check.

    Raises:
        TypeError: If any element in data_list is not an int or float.

    Example:
        check_list_items_are_numbers([1, 2.5, 3])  # Passes
        check_list_items_are_numbers(['a', 2, 3])  # Raises TypeError
        check_list_items_are_numbers(None)         # Passes
    """
    if data_list is None:
        return

    for x in data_list:
        if not isinstance(x, (int, float)):
            raise TypeError('All elements must be numbers')



    












