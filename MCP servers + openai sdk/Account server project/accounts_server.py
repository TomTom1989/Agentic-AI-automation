from mcp.server.fastmcp import FastMCP
from dataclasses import dataclass, field
import json, pathlib

DB = pathlib.Path("accounts.json").resolve()
DB.write_text(json.dumps({"Tom": {"balance": 10_000, "holdings": {}}}, indent=2))

@dataclass
class Account:
    name: str
    balance: float
    holdings: dict[str, int] = field(default_factory=dict)

    @classmethod
    def get(cls, name: str) -> "Account":
        data = json.loads(DB.read_text())[name]
        return cls(name, data["balance"], data["holdings"])

    def _persist(self):
        db = json.loads(DB.read_text())
        db[self.name] = {"balance": self.balance, "holdings": self.holdings}
        DB.write_text(json.dumps(db, indent=2))

    def buy(self, symbol: str, qty: int):
        cost = qty * 100        # <-- dummy fixed price
        if cost > self.balance:
            raise ValueError("Not enough cash")
        self.balance -= cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + qty
        self._persist()
        return self.balance

mcp = FastMCP("accounts")

@mcp.tool()
async def get_balance(name: str) -> float:
    return Account.get(name).balance

@mcp.tool()
async def buy_shares(name: str, symbol: str, qty: int) -> float:
    return Account.get(name).buy(symbol, qty)

@mcp.resource("accounts://{name}")
async def read_account(name: str) -> str:
    return json.dumps(Account.get(name).__dict__, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")
