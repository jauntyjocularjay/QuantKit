# QuantKit

A collection of python utilities I created because why in Hades are these not already implemented in the standard library?

## Table of Contents

- [LLM Disclosure](#llm-disclosure)
- [`stats.py`](#statspy)
  - [`median_index`](#median_index)
  - [`interquartile_slice`](#interquartile_slice)
  - [`iqs`](#iqs)
  - [`binom`](#binom)
  - [`nck`](#nck)
  - [`geom`](#geom)
  - [`geoh`](#geoh)
  - [`pois`](#pois)
  - [Constants](#constants)
- [Test Runner](#test-runner)
  - [Bash](#bash)
  - [PowerShell](#powershell)

## LLM Disclosure

All working base code is written by an actual human, [@jauntyjocularjay](https://github.com/jauntyjocularjay). LLM @Copilot is used to author documentation, docstrings, and unit tests with editing and fine tuning by @jauntyjocularjay.

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

Computes geometric distribution statistics: probability of first success at trial `k`, mean, and standard deviation. Supports both definitions — counting the trial of first success (`includes_success=True`, default) or counting failures before first success (`includes_success=False`).

```python
from quantkit.stats import geom
result = geom(p=Fraction(1, 6), k_trials=3)
result[VALUE]       # probability as a Fraction
result[MEAN]        # expected trials as a Fraction
result[STD_DEV][FRAC_STR] # standard deviation as a symbolic string
result[STD_DEV][FLOAT]    # standard deviation as a float
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

---

## Test Runner

### Bash

```bash
# Run from the project root (the parent of quantkit)
$ cd path/to/module/parent

# Run a specific test file
$ poetry run pytest -v quantkit/test_stats.py

# Run tests with coverage report
$ poetry run pytest --cov=quantkit --cov-report=term -v quantkit/test_stats.py
```

### PowerShell

```powershell
# Run from the project root (the parent of quantkit)
cd path\to\module\parent

# Run a specific test file
poetry run pytest -v quantkit/test_stats.py

# Run tests with coverage report
poetry run pytest --cov=quantkit --cov-report=term -v quantkit/test_stats.py
```

All tests are DRY, readable, and use the latest API and key constants. See `test_stats.py` for examples.
