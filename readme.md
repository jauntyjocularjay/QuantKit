# QuantKit

## Table of Contents

- [LLM Disclosure](#llm-disclosure)
- [Overview](#overview)
- [Installation](#installation)
- [`constants.py`](#constantspy)
- [`boxplot.py`](#boxplotpy)
  - [`BoxPlot`](#boxplot)
  - [Example output](#example-output)
- [`stats.py`](#statspy)
  - [`median_index`](#median_index)
  - [`interquartile_slice`](#interquartile_slice)
  - [`iqs`](#iqs)
  - [`binom`](#binom)
  - [`nck`](#nck)
  - [`geom`](#geom)
  - [`geom_mean`](#geom_mean)
  - [`geom_var`](#geom_var)
  - [`geoh`](#geoh)
  - [`pois`](#pois)
- [`pytilities/`](#pytilities)
- [Test Runner](#test-runner)
  - [Bash](#bash)

## LLM Disclosure

All working base code is written by an actual human, [@jauntyjocularjay](https://github.com/jauntyjocularjay). LLM @Copilot is used to author documentation, docstrings, and unit tests with editing and fine tuning by @jauntyjocularjay.

## Overview

QuantKit is a small collection of Python utilities for numeric analysis, descriptive statistics, and probability calculations. The repository is organized around a few focused modules:

- `stats.py`: probability distributions and sequence helpers.
- `boxplot.py`: a `BoxPlot` summary object for quick exploratory analysis.
- `constants.py`: named constants used to avoid repeated string literals.
- `pytilities/`: validation and helper utilities used throughout the project.

The code is intentionally lightweight and dependency-free aside from the dev/test stack in `requirements.txt`.

## Installation

Clone the repository and install the project dependencies from the repo root:

```bash
git clone https://github.com/jauntyjocularjay/QuantKit.git
cd QuantKit
git submodule update --init --recursive
python -m pip install -r requirements.txt
```

From there, run the tests directly with `pytest` from the project root:

```bash
python -m pytest -v
```

If you are importing modules locally, run Python from the repository root or add the repository root to `PYTHONPATH`.

## `constants.py`

`constants.py` centralizes the string keys and symbolic enums used across QuantKit. These names are exported as module-level constants so callers can avoid repeating magic strings and keep dictionary access consistent.

```python
from quantkit.constants import (
    OUTCOME,
    ALL_OUTCOMES,
    PROBABILITY,
    COMPLEMENT,
    MEAN,
    VALUE,
    COEF,
    STD_DEV,
    FRAC,
    FRAC_STR,
    FLOAT,
    Symbol,
    EventType,
    Relationship,
)
```

The module also defines reusable enums for probability relationships and event types:

- `Symbol`: set and logic symbols such as `∪`, `∩`, and `|`
- `EventType`: `DEPENDENT`, `INDEPENDENT`, and `MUTUAL_EXCLUSIVE`
- `Relationship`: symbolic relationship operators for probability expressions

## `boxplot.py`

`boxplot.py` defines a `BoxPlot` dataclass that computes a five-number summary for a numeric sequence and exposes the IQR, range, outliers, and Tukey fence.

### `BoxPlot`

```python
from quantkit.boxplot import BoxPlot

bp = BoxPlot([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(bp.min)       # 1
print(bp.q1)        # 3.0
print(bp.median)    # 5
print(bp.q3)        # 7.0
print(bp.max)       # 9
print(bp.outliers)  # []
print(bp.as_dict())
```

The constructor accepts a numeric sequence and an optional quartile method:

```python
BoxPlot(data_list, quantile_method='exclusive')
```

The supported quartile methods are the same ones accepted by Python's `statistics.quantiles`, and the class stores the sorted input data alongside the summary values.

### Example output

```python
bp = BoxPlot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
print(bp)
# boxplot:    min * 1 ---- q1 [ 3.25     median | 6.5     q3 ] 9.75 ---- max * 12]
```

The object also exposes:

- `tukey_fence`: lower and upper whisker bounds using the 1.5x IQR rule.
- `iqr`: interquartile range.
- `range`: max minus min.
- `outliers`: values outside the Tukey fence.
- `as_dict()`: dictionary-friendly representation for logging or serialization.

## `stats.py`

`stats.py` is a custom statistics library with utilities for exploratory data analysis and probability distributions. All dictionary keys are defined as constants in `constants.py` to avoid string literals and reduce errors.

### `median_index`

Finds the median value(s) in a sorted sequence and returns a tuple of indices. Odd-length sequences return a single index; even-length sequences return two indices.

```python
median_index([1, 2, 3, 4, 5, 6, 7])  # returns (3,)
median_index([1, 2, 3, 4, 5, 6])     # returns (2, 3)
```

### `interquartile_slice`

Returns the data points within the interquartile range (IQR) of the input sequence using index-based slicing (not interpolation). This is the actual data in the "middle 50%" of the sorted sequence. Preserves the original input type (list, set, or tuple).

```python
interquartile_slice([1, 2, 3, 4, 5, 6, 7, 8, 9])  # returns [3, 4, 5, 6, 7]
```

### `iqs`

Alias for `interquartile_slice`.

### `binom`

Computes binomial distribution statistics: probability, binomial coefficient, mean, and standard deviation.

```python
from quantkit.stats import binom
result = binom(p=Fraction(1, 2), n_trials=10, k_success=3)
result[VALUE]       # probability as a Fraction
result[COEF]        # binomial coefficient C(n, k)
result[MEAN]        # expected successes
result[STD_DEV][FRAC]  # standard deviation as a symbolic string
result[STD_DEV][FLOAT] # standard deviation as a float
```

### `nck`

Computes the binomial coefficient $C(n, k)$ as an exact `Fraction`.

```python
from quantkit.stats import nck
nck(10, 3)  # Fraction(120, 1)
```

### `geom`

Computes the geometric PMF value at `k_trials` for a success probability `p`.
Supports both definitions of the geometric variable:

- `includes_success=True` (default): `k_trials` is the trial index of the first success.
- `includes_success=False`: `k_trials` is the number of failures before the first success.

```python
from quantkit.stats import geom
geom(p=Fraction(1, 6), k_trials=3)  # Fraction PMF value
```

### `geom_mean`

Computes the mean of the geometric distribution for the selected definition.

```python
from quantkit.stats import geom_mean
geom_mean(Fraction(1, 6), includes_success=True)   # 1/p
geom_mean(Fraction(1, 6), includes_success=False)  # (1-p)/p
```

### `geom_var`

Computes the variance of the geometric distribution, `Var = (1-p)/p^2`.

```python
from quantkit.stats import geom_var
geom_var(Fraction(1, 6))
```

### `geoh`

Computes a hypergeometric point probability using population-of-interest size, remaining population size, sample size, and target successes.

```python
from quantkit.stats import geoh
geoh(pop_i=80, pop_b=100, n_trials=50, k_success=35)
```

### `pois`

Computes the Poisson point probability $P(X=x)$ for a given mean. Includes validation and a dynamic overflow check to avoid unsafe floating-point exponentiation for large inputs.

```python
from quantkit.stats import pois
pois(x=3, mean=2)  # 0.180447...
```

---

All dictionary keys are defined as constants in `constants.py`. Use these for all key access to avoid typos and string duplication. These are exportable into your projects.

```python
VALUE = 'value'
COEF  = 'coefficient'
MEAN  = 'mean'
STD_DEV = 'std_dev'
FRAC  = 'fraction'
FRAC_STR = 'fraction_string'
FLOAT = 'float'
```

## `pytilities/`

The repository also includes `pytilities/`, a helper package for validation, sequence conversion, and console utilities used by the main modules. The subpackage is documented in [pytilities/readme.md](pytilities/readme.md) and contains reusable pieces such as:

- `validation.py`: type and bounds checks
- `returns.py`: sequence reconstruction helpers
- `console.py`: terminal clearing utilities
- `assert_helpers.py`: shared pytest assertion helpers

## Test Runner

All tests are DRY, readable, and use the latest API and key constants. See `test_stats.py` for examples.

### Bash

```bash
# Run from the project root
cd path/to/QuantKit

# Run a specific test file
python -m pytest -v test_stats.py

# Run tests with coverage report
python -m pytest --cov=. --cov-report=term -v test_stats.py
```

