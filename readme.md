# PyTils

A collection of python utilities I created because why in Hades are these not already implemented in the standard library?

## `console`

### `console.clear()`

`console.clear()` clears the python console. Why would I want to see old data? If I want to compare data, I will print it to the console.


## `stats`

`stats` is a custom statistics library with robust, readable, and DRY utilities for exploratory data analysis and box plot statistics. All dictionary keys are defined as constants (e.g., `SEQUENCE_MINIMUM`, `Q1`, etc.) to avoid string literals and reduce errors.

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

### Key Constants

All dictionary keys are defined as constants in `stats.py` and listed below. Use these for all key access to avoid typos and string duplication. These are exportable into your projects.

- DATA_LIST = 'data_list'
- SEQUENCE_MINIMUM = 'min'
- SEQUENCE_MAXIMUM = 'max'
- SEQUENCE_MEDIAN = 'median'
- SEQUENCE_RANGE = 'range'
- OUTLIERS = 'outliers'
- Q1 = 'q1'
- Q2 = 'q2'
- Q3 = 'q3'
- IQR = 'iqr'
- TUKEY_FENCE = 'tukey_fence'

### Robust Imports

`stats.py` uses a robust import pattern for `console` so it works both as a script and as a package, regardless of your shell or IDE.

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
