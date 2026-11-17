# Expense Splitter Project Documentation

## Overview

This repository documents the development of a Python `ExpenseSplitter` module through zero-shot prompting, few-shot prompting, and step-by-step debugging. The project includes the initial floating-point implementation, a docstring-enhanced implementation, a unit-test suite, and a bug-fixed implementation that stores balances in integer cents.

## Project files

| File | Purpose |
| --- | --- |
| `expense_splitter.py` | Initial implementation using floating-point balances. |
| `expense_splitter (2nd prompt).py` | Same behavior with structured method docstrings. |
| `expense_splitter (bug fixed).py` | Corrected implementation using integer cents and remainder allocation. |
| `test_expense_splitter.py` | Tests for registration, validation, splits, transfers, and balance totals. |
| `test_expense_splitter (bug fixed).py` | Extended tests covering exact-cent behavior. |

## Screenshot evidence

The following sections use the supplied image names as titles. Store the screenshots in a `screenshots/` directory using these exact filenames so GitHub renders them from the links below.

### `zero shot prompt.png`

![zero shot prompt.png](screenshots/zero%20shot%20prompt.png)

The initial prompt requests an `ExpenseSplitter` class with methods for registering people, recording expenses, reading balances, and simplifying debts. It also specifies standard-library-only Python, type hints, and no docstrings in the first version.

### `response of zero shot prompt.png`

![response of zero shot prompt.png](screenshots/response%20of%20zero%20shot%20prompt.png)

The generated response creates the first `expense_splitter.py` implementation. It validates inputs, updates payer and participant balances, and uses a heap-based settlement algorithm.

### `zero shot prompt (test case).png`

![zero shot prompt (test case).png](screenshots/zero%20shot%20prompt%20(test%20case).png)

The testing prompt asks for `unittest` coverage of registration, invalid inputs, two- and three-person splits, debt simplification, and the invariant that balances sum to zero.

### `few shot prompt.png`

![few shot prompt.png](screenshots/few%20shot%20prompt.png)

The few-shot prompt defines the required documentation style: a summary line followed by `Args`, `Returns`, and `Raises` sections where applicable.

### `response of few shot prompt.png`

![response of few shot prompt.png](screenshots/response%20of%20few%20shot%20prompt.png)

The response adds docstrings to every method and explains the validation rules, rounding behavior, and the greedy debt-settlement strategy.

### `chain of thoughts prompt.png`

![chain of thoughts prompt.png](screenshots/chain%20of%20thoughts%20prompt.png)

The debugging prompt presents a failing test involving three expenses of 33.33, 33.33, and 33.34, and asks for the source of the one-cent discrepancy.

### `chain of thoughts response.png`

![chain of thoughts response.png](screenshots/chain%20of%20thoughts%20response.png)

The response identifies two separate issues: the expected total should represent the amount owed rather than the gross amount paid, and independent floating-point rounding can leave a one-cent imbalance.

## Implementation details

### Balance model

For each expense, the payer receives credit for the full amount and every participant receives an equal debit. A positive balance means that the person should receive money; a negative balance means that the person owes money.

The original versions store balances as `float` values. The corrected version stores integer cents instead:

1. Convert the input amount to cents once.
2. Divide cents among participants with `divmod`.
3. Assign any remainder cents deterministically to the first participants.
4. Return values as dollars only at the public API boundary.

This ensures that each expense preserves the exact cent total and that the sum of all balances remains zero.

### Debt simplification

`simplify_debts()` places creditors and debtors into heaps, repeatedly matches the largest outstanding creditor with the largest outstanding debtor, and emits tuples in the form:

```python
(debtor, creditor, amount)
```

The algorithm produces a compact settlement in practice and uses integer cents internally in the corrected implementation.

## Testing

Run the test suites with:

```bash
python -m unittest -v test_expense_splitter.py
python -m unittest -v "test_expense_splitter (bug fixed).py"
```

The corrected test suite adds an uneven-split regression test. Three expenses totaling 100.00 are split among three people, and the test verifies that the balances sum to exactly zero cents and that the transfers total 66.66 rather than losing a cent through floating-point rounding.

## Lessons learned

- A test expectation must match the domain model: the payer’s net amount owed is not the same as the gross amount paid.
- Floating-point values are unsuitable for exact currency accounting when intermediate rounding is required.
- Integer cents provide a simple and reliable representation for financial calculations.
- Prompt examples can standardize generated documentation and make the result easier to review.
