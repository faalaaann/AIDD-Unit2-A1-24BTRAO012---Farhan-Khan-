import heapq


class ExpenseSplitter:
    def __init__(self) -> None:
        self._balances: dict[str, float] = {}

    def add_person(self, name: str) -> None:
        if name in self._balances:
            raise ValueError(f"Person already registered: {name!r}")
        self._balances[name] = 0.0

    def add_expense(self, payer: str, amount: float, participants: list[str]) -> None:
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
        if person not in self._balances:
            raise ValueError(f"Unknown person: {person!r}")
        return round(self._balances[person], 2)

    def all_balances(self) -> dict[str, float]:
        return {name: round(bal, 2) for name, bal in self._balances.items()}

    def simplify_debts(self) -> list[tuple[str, str, float]]:
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
