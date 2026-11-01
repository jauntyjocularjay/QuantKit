# QuantKit Improvement Checklist

This checklist captures the main recommendations from the project review and explains why each item matters. These are proposed improvements for maintainability, correctness, and test coverage; they are not a record of completed work.

## 1) Clean up module imports and dependency visibility

- [x] Remove or reduce wildcard imports in the project code
  - Why: `from .stats import *`, `from .constants import *`, and similar patterns hide the actual dependencies of each module. This makes the code harder to read, harder to refactor, and harder for static analysis tools to verify.
  - Example impact: it becomes unclear which symbols are truly required by a module, and names can accidentally collide across imports.

- [ ] Make module boundaries more explicit
  - Why: [stats.py](stats.py) currently contains probability helpers, sequence-analysis utilities, and validation-adjacent logic. Splitting or documenting responsibilities would make the package easier to maintain and extend.

## 2) Standardize validation behavior

- [ ] Standardize validation contracts and error semantics across the library
  - Why: some functions raise custom exceptions for invalid sequences, while others accept `None` or silently pass through edge cases. This makes the API less predictable.
  - Goal: make each function follow the same rule: validate inputs early, raise a consistent exception type, and document the contract clearly.

- [ ] Tighten type checks for probability parameters
  - Why: probability values should be validated as finite numbers in the valid range `(0, 1)`. This helps avoid subtle bugs where invalid numeric values slip through.
  - Example concern: float conversion and `Fraction` coercion are mathematically precise, but the validations should be stricter and more explicit.

- [ ] Tighten type checks for integer inputs and trial counts
  - Why: values like `n_trials`, `k_success`, and distribution parameters should be validated as proper integers or non-negative values when required.
  - Goal: reject malformed inputs before they reach computation paths that may fail unexpectedly or produce nonsensical probabilities.

- [ ] Reject `bool` values consistently
  - Why: in Python, `bool` is a subclass of `int`, which can allow boolean values to sneak through validation that only checks `int` or `float`. This is a common source of edge-case bugs.
  - Example: a value like `True` may be treated as `1` in a probability or count context, which is not usually intended.

## 3) Strengthen test coverage around edge cases

- [ ] Add tests for boolean-like values in numeric sequences and probability checks
  - Why: these are easy to overlook, but they are especially important in validation-heavy statistical code. A bool slipping through may produce mathematically valid results but semantically invalid behavior.

- [ ] Add tests for invalid trial counts and impossible distribution parameters
  - Why: boundary conditions such as negative values, `k_success > n_trials`, and zero/negative populations should be covered directly.
  - Goal: ensure the library fails fast and consistently for impossible inputs.

- [ ] Add explicit tests for malformed numeric input and `None` handling
  - Why: sequence validation should be exercised for cases such as non-sequence input, `None`, non-numeric entries, and `NaN` / `inf` values.

## 4) Improve maintainability without changing public behavior

- [ ] Reduce mixed responsibilities inside statistical utility modules
  - Why: combining probability distribution functions, data-sequence logic, and validation helpers makes updates riskier and harder to review.
  - Recommended direction: keep public APIs intact while separating validation helpers and statistical logic more clearly when practical.

- [ ] Preserve the existing public API while improving consistency
  - Why: the library is small but already exposes several helper functions and validation utilities. Refactoring should improve clarity without breaking users unnecessarily.

## 5) Suggested implementation order

- [ ] Begin with validation consistency and bool rejection
- [ ] Add regression tests for invalid numeric and distribution edge cases
- [ ] Refactor imports and clarify module boundaries
- [ ] Re-run the project test suite and confirm behavior remains stable

This checklist is intended as a practical path toward cleaner, safer, and easier-to-maintain code. It reflects review feedback rather than a declaration of completed work.
