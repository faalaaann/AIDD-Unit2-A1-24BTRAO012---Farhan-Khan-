# Expense Splitter Python Module

A small Python project that demonstrates how prompting approaches can be used to create, document, test, and debug an `ExpenseSplitter` class.

## Contents

- `expense_splitter.py` - initial implementation using floating-point balances.
- `expense_splitter (2nd prompt).py` - implementation with method docstrings.
- `expense_splitter (bug fixed).py` - corrected implementation using integer cents to avoid rounding drift.
- `test_expense_splitter.py` - unit tests for the original implementation.
- `test_expense_splitter (bug fixed).py` - tests including the uneven-cent regression case.
- [`document.md`](document.md) - full project documentation and prompt screenshots.

## Features

- Register people and reject duplicate names.
- Record expenses shared equally among registered participants.
- Validate unknown payers, unknown participants, empty participant lists, duplicate participants, and invalid amounts.
- Read one person’s balance or all balances.
- Generate transfers that settle debts by matching creditors and debtors.
- Keep monetary calculations exact to the cent in the bug-fixed version.

## Run the tests

From the repository directory:

```bash
python -m unittest -v test_expense_splitter.py
python -m unittest -v "test_expense_splitter (bug fixed).py"
```

The bug-fixed implementation is stored as a separate file for comparison. To test it as `expense_splitter`, copy it to a temporary directory or rename it locally before running the corresponding test file.

## Documentation screenshots

The complete explanation, including the supplied prompt and response screenshots, is in [`document.md`](document.md). Screenshot files should be stored in `screenshots/` with the exact filenames used in that document.
