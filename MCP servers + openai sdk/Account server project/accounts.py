# accounts.py  ────────────────────────────────────────────────────────────────
from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar, Dict


@dataclass
class Account:
    # ── instance data ────────────────────────────────────────────────────────
    name: str
    balance: float = 10_000.0           # start with 10 000 $ cash
    holdings: Dict[str, int] = field(default_factory=dict)
    strategy: str = "buy-and-hold"

    # ── class-level registry so we can fetch by name ────────────────────────
    _registry: ClassVar[Dict[str, "Account"]] = {}

    # automatically register on creation
    def __post_init__(self):
        Account._registry[self.name.lower()] = self

    # ── convenience look-ups ────────────────────────────────────────────────
    @classmethod
    def get(cls, name: str) -> "Account":
        if name.lower() not in cls._registry:
            raise KeyError(f"unknown account {name!r}")
        return cls._registry[name.lower()]

    # ── simple portfolio operations ─────────────────────────────────────────
    def buy_shares(self, symbol: str, qty: int, rationale: str | None = None) -> float:
        self.balance -= 100 * qty        # <<— pretend every share costs $100
        self.holdings[symbol] = self.holdings.get(symbol, 0) + qty
        return self.balance

    def sell_shares(self, symbol: str, qty: int, rationale: str | None = None) -> float:
        if self.holdings.get(symbol, 0) < qty:
            raise ValueError("not enough shares")
        self.balance += 100 * qty
        self.holdings[symbol] -= qty
        return self.balance

    def change_strategy(self, strategy: str) -> str:
        self.strategy = strategy
        return self.strategy

    # ── helpers used by MCP resources ───────────────────────────────────────
    def report(self) -> str:
        return {
            "name": self.name,
            "balance": self.balance,
            "holdings": self.holdings,
            "strategy": self.strategy,
        }

    def get_strategy(self) -> str:
        return self.strategy


# ── seed a couple of demo accounts so the tool has something to query ───────
Account("Alice")
Account("Bob")
