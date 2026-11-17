import unittest

from expense_splitter import ExpenseSplitter


class TestExpenseSplitter(unittest.TestCase):
    def setUp(self) -> None:
        self.splitter = ExpenseSplitter()

    def _register(self, *names: str) -> None:
        for name in names:
            self.splitter.add_person(name)

    def test_register_person(self) -> None:
        self.splitter.add_person("Alice")
        self.assertEqual(self.splitter.balance("Alice"), 0.0)
        self.assertEqual(self.splitter.all_balances(), {"Alice": 0.0})

    def test_duplicate_registration_raises(self) -> None:
        self.splitter.add_person("Alice")
        with self.assertRaises(ValueError):
            self.splitter.add_person("Alice")

    def test_simple_two_person_split(self) -> None:
        self._register("Alice", "Bob")
        self.splitter.add_expense("Alice", 100.0, ["Alice", "Bob"])
        self.assertAlmostEqual(self.splitter.balance("Alice"), 50.0)
        self.assertAlmostEqual(self.splitter.balance("Bob"), -50.0)

    def test_three_person_split(self) -> None:
        self._register("Alice", "Bob", "Carol")
        self.splitter.add_expense("Alice", 90.0, ["Alice", "Bob", "Carol"])
        self.assertAlmostEqual(self.splitter.balance("Alice"), 60.0)
        self.assertAlmostEqual(self.splitter.balance("Bob"), -30.0)
        self.assertAlmostEqual(self.splitter.balance("Carol"), -30.0)

    def test_unknown_payer_raises(self) -> None:
        self._register("Alice")
        with self.assertRaises(ValueError):
            self.splitter.add_expense("Zed", 10.0, ["Alice"])

    def test_empty_participants_raises(self) -> None:
        self._register("Alice")
        with self.assertRaises(ValueError):
            self.splitter.add_expense("Alice", 10.0, [])

    def test_zero_amount_raises(self) -> None:
        self._register("Alice", "Bob")
        with self.assertRaises(ValueError):
            self.splitter.add_expense("Alice", 0.0, ["Alice", "Bob"])

    def test_negative_amount_raises(self) -> None:
        self._register("Alice", "Bob")
        with self.assertRaises(ValueError):
            self.splitter.add_expense("Alice", -20.0, ["Alice", "Bob"])

    def test_simplify_debts_sums_to_total_owed(self) -> None:
        self._register("Alice", "Bob", "Carol", "Dave")
        self.splitter.add_expense("Alice", 100.0, ["Alice", "Bob", "Carol", "Dave"])
        self.splitter.add_expense("Bob", 60.0, ["Bob", "Carol"])
        self.splitter.add_expense("Carol", 45.0, ["Alice", "Bob", "Carol"])

        balances = self.splitter.all_balances()
        total_owed = sum(-b for b in balances.values() if b < 0)

        transfers = self.splitter.simplify_debts()
        self.assertAlmostEqual(sum(amount for _, _, amount in transfers), total_owed, places=2)

        # Applying the transfers should settle everyone.
        settled = dict(balances)
        for debtor, creditor, amount in transfers:
            self.assertGreater(amount, 0)
            settled[debtor] += amount
            settled[creditor] -= amount
        for name, bal in settled.items():
            self.assertAlmostEqual(bal, 0.0, places=2, msg=name)

    def test_uneven_split_balances_sum_to_exactly_zero(self) -> None:
        self._register("A", "B", "C")
        self.splitter.add_expense("A", 33.33, ["A", "B", "C"])
        self.splitter.add_expense("A", 33.33, ["A", "B", "C"])
        self.splitter.add_expense("A", 33.34, ["A", "B", "C"])
        balances = self.splitter.all_balances()
        self.assertEqual(round(sum(balances.values()) * 100), 0)
        total_owed = sum(b for b in balances.values() if b > 0)
        transfers = self.splitter.simplify_debts()
        # A paid 100.00 and bears 33.34 of it (the odd cent goes to the first
        # participant), so exactly 66.66 must move.
        self.assertAlmostEqual(total_owed, 66.66, places=2)
        self.assertAlmostEqual(sum(t[2] for t in transfers), total_owed, places=2)

    def test_simplify_debts_no_debts(self) -> None:
        self._register("Alice", "Bob")
        self.assertEqual(self.splitter.simplify_debts(), [])

    def test_balances_sum_to_zero_after_several_expenses(self) -> None:
        self._register("Alice", "Bob", "Carol")
        self.splitter.add_expense("Alice", 100.0, ["Alice", "Bob", "Carol"])
        self.splitter.add_expense("Bob", 33.33, ["Alice", "Bob"])
        self.splitter.add_expense("Carol", 47.5, ["Alice", "Bob", "Carol"])
        self.splitter.add_expense("Alice", 12.0, ["Carol"])
        total = sum(self.splitter.all_balances().values())
        self.assertEqual(round(total * 100), 0)


if __name__ == "__main__":
    unittest.main()
