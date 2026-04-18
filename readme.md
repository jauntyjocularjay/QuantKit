# PyTils

A collection of python utilities I created because why in Hades are these not already implemented in the standard library?

## `console`

### `console.clear()`

`console.clear()` clears the python console. Why would I want to see old data? If I want to compare data, I will print it to the console.

## `stats`

`stats` is a custom statistics library that stores non-standard functions created while I was learning about statistics.

### `median_index`

`median_index` looks for the median value (or closest to) in a list and provides a tuple of indices where that median is found. For an odd-number list, a single value in a tuple. For an even number list, a two-value tuple.

### `iqr_slice`

Returns the data points within the interquartile range (IQR) of the input list using index-based slicing.

This function sorts the input data and returns a slice containing the "middle 50%" of values, i.e., those between the lower and upper quartiles, using integer indices (no interpolation). This is not the standard IQR value (Q3 - Q1), but rather the actual data points that fall within the IQR range. Useful for exploratory data analysis and visualizations where you want to examine or plot the spread of the central data.

**Parameters:**
- `data_list` (list, optional): The input list of numeric values.

**Returns:**
- `list` or `None`: A slice of the sorted data representing the interquartile range, or `None` if the input is `None` or empty.

**Example:**
```python
iqr_slice([1, 2, 3, 4, 5, 6, 7, 8, 9])  # returns [3, 4, 5, 6, 7]
```

** Test Runner

```bash
$ cd path/to/module

# Run a specific test file
$ poetry run pytest -v test_stats.py

# Run tests with coverage  report
$ poetry run pytest --cov=PyTils --cov-report=term -v test_stats.py
```

