# PyTils

A collection of python utilities I created because why in Hades are these not already implemented in the standard library?

## LLM Disclosure

All working base code is written by an actual human, [@jauntyjocularjay](https://github.com/jauntyjocularjay). LLM @Copilot is used to author documentation, docstrings, and unit tests with editing and fine tuning by @jauntyjocularjay.

## `console.py`

### `console.clear()`

`console.clear()` clears the python console. Why would I want to see old data? If I want to compare data, I will print it to the console.

## `stats.py`

`stats.py` is a custom statistics library with robust, readable, and DRY utilities for exploratory data analysis and box plot statistics. All dictionary keys are defined as constants to avoid string literals and reduce errors.

### `median_index`

Finds the median value(s) in a list and returns a tuple of indices. Odd-length lists return a single index; even-length lists return two indices.

### `interquartile_slice`

Returns the data points within the interquartile range (IQR) of the input list using index-based slicing (not interpolation). This is the actual data in the "middle 50%" of the sorted list.

**Example:**

```python
interquartile_slice([1, 2, 3, 4, 5, 6, 7, 8, 9])  # returns [3, 4, 5, 6, 7]
```

### `BoxPlot`

`BoxPlot` computes a robust five-number summary and Tukey outlier fences for a numeric sequence. It uses key constants for all dictionary outputs and properties. Whiskers (min/max) are the most extreme values within the Tukey fences, or the sequence extremes if all values are outliers.

**Example:**
```python
from PyTils.stats import BoxPlot
bp = BoxPlot([1, 2, 3, 4, 5, 6])
print(bp.as_dict())
# { 'min': 1, 'q1': 2.25, 'median': 3.5, 'q2': 3.5, 'q3': 4.75, 'max': 6, ... }
```


### `BoxPlot.__str__()`

The `__str__` method of `BoxPlot` provides a compact, human-readable summary of the five-number summary and whiskers:

```
boxplot:    min * {min} ---- q1 [ {q1}     median | {median}     q3 ] {q3} ---- max * {max}]
```

This format is useful for quick inspection in logs or printouts, showing the minimum, first quartile (q1), median, third quartile (q3), and maximum values. For a more detailed or traditional output, use `BoxPlot.as_dict()`.

**Example:**
```python
from PyTils.stats import BoxPlot
bp = BoxPlot([1, 2, 3, 4, 5, 6])
print(str(bp))
# boxplot:    min * 1 ---- q1 [ 2.25     median | 3.5     q3 ] 4.75 ---- max * 6]
```

---

All dictionary keys are defined as constants in `stats.py` and listed below. Use these for all key access to avoid typos and string duplication. These are exportable into your projects.

```python
DATA_LIST = 'data_list'
SEQUENCE_MINIMUM = 'min'
SEQUENCE_MAXIMUM = 'max'
SEQUENCE_MEDIAN = 'median'
SEQUENCE_RANGE = 'range'
OUTLIERS = 'outliers'
Q1 = 'q1'
Q2 = 'q2'
Q3 = 'q3'
IQR = 'iqr'
TUKEY_FENCE = 'tukey_fence'
```

---

## Test Runner

### Bash

```bash
# !!!IMPORTANT!!! run the test scripts from the project root (the parent of PyTils)
$ cd path/to/module/parent

# Run a specific test file
$ poetry run pytest -v PyTils/tests/test_stats.py

# Run tests with coverage report
$ poetry run pytest --cov=PyTils --cov-report=term -v PyTils/tests/test_stats.py
```

### PowerShell

```powershell
# PowerShell: run from the project root (the parent of PyTils)
cd path\to\module\parent

# Run a specific test file
poetry run pytest -v PyTils/tests/test_stats.py

# Run tests with coverage report
poetry run pytest --cov=PyTils --cov-report=term -v PyTils/tests/test_stats.py
```

All tests are DRY, readable, and use the latest API and key constants. See `tests/test_stats.py` for examples.

## ListSet Checklist

### Mutator Methods

- [ ] Assignment (__setitem__ and slice assignment): Users can do lst[2] = x or lst[1:3] = [x, y]. You should override these to enforce uniqueness.
- [ ] In-place addition (__iadd__): lst += [x, y] should also check for duplicates.
- [ ] Multiplication (__imul__): lst *= n could introduce duplicates if not blocked or handled.
- [ ] Copying and Construction Methods like copy() or using the constructor with an existing ListSet should preserve uniqueness.

### Performance

- [ ] self.count(x) is O(n). For large lists, consider maintaining an internal set for O(1) membership checks, but this adds complexity.

### Equality and Hashing

- [ ] If you want ListSet([1,2]) == ListSet([2,1]) to be True, you’ll need to override __eq__. Otherwise, it will behave like a list (order matters).

### Documentation

- [ ] Clearly document that your class enforces uniqueness and how it handles order.

### Testing

- [ ] Test all mutating methods, including edge cases (e.g., inserting at various positions, slice assignment, etc).