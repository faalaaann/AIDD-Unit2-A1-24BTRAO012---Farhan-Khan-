import heapq


class ExpenseSplitter:
    def __init__(self) -> None:
        """Create an empty splitter with no registered people."""
        self._balances: dict[str, float] = {}

    def add_person(self, name: str) -> None:
        """Register a person so they can pay for or share expenses.

        Args:
            name: Unique name of the person to register.

        Raises:
            ValueError: If the person is already registered.
        """
        if name in self._balances:
            raise ValueError(f"Person already registered: {name!r}")
        self._balances[name] = 0.0

    def add_expense(self, payer: str, amount: float, participants: list[str]) -> None:
        """Record an expense split equally among participants.

        Args:
            payer: Name of the person who paid.
            amount: Total amount paid (must be positive).
            participants: People sharing the expense, including the payer.

        Raises:
            ValueError: If the payer or any participant is not registered,
                amount <= 0, or participants is empty or contains duplicates.
        """
        if payer not in self._balances:
            raise ValueError(f"Unknown payer: {payer!r}")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not participants:
            raise ValueError("Participants must not be empty")
        if len(set(participants)) != len(participants):
            raise ValueError("Duplicate participants")
        for p in participants:
            if p not in self._balances:
                raise ValueError(f"Unknown participant: {p!r}")

        share = amount / len(participants)
        self._balances[payer] += amount
        for p in participants:
            self._balances[p] -= share

    def balance(self, person: str) -> float:
        """Return the net balance of a person.

        Args:
            person: Name of the registered person.

        Returns:
            Positive if the person is owed money, negative if they owe money,
            rounded to two decimal places.

        Raises:
            ValueError: If the person is not registered.
        """
        if person not in self._balances:
            raise ValueError(f"Unknown person: {person!r}")
        return round(self._balances[person], 2)

    def all_balances(self) -> dict[str, float]:
        """Return the net balance of every registered person.

        Returns:
            Mapping of person name to net balance (positive if owed money,
            negative if they owe money), rounded to two decimal places.
        """
        return {name: round(bal, 2) for name, bal in self._balances.items()}

    def simplify_debts(self) -> list[tuple[str, str, float]]:
        """Compute a small set of transfers that settles all debts.

        Repeatedly matches the largest creditor with the largest debtor, which
        yields at most one fewer transfer than the number of people with a
        non-zero balance. Amounts are computed in integer cents.

        Returns:
            List of (debtor, creditor, amount) tuples, where each debtor pays
            the creditor the given amount.
        """
        # Work in integer cents to avoid floating-point drift.
        creditors: list[tuple[int, str]] = []
        debtors: list[tuple[int, str]] = []
        for name, bal in self._balances.items():
            cents = round(bal * 100)
            if cents > 0:
                heapq.heappush(creditors, (-cents, name))
            elif cents < 0:
                heapq.heappush(debtors, (cents, name))

        transfers: list[tuple[str, str, float]] = []
        while creditors and debtors:
            neg_credit, creditor = heapq.heappop(creditors)
            neg_debt, debtor = heapq.heappop(debtors)
            credit = -neg_credit
            debt = -neg_debt
            settled = min(credit, debt)
            transfers.append((debtor, creditor, settled / 100))
            if credit > settled:
                heapq.heappush(creditors, (-(credit - settled), creditor))
            if debt > settled:
                heapq.heappush(debtors, (-(debt - settled), debtor))
        return transfers
