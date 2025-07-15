class Account:
    def __init__(self, username: str, initial_deposit: float):
        """
        Initializes a new account with a username and an initial deposit.
        
        :param username: The name of the user for the account.
        :param initial_deposit: The initial amount of money deposited into the account.
        """
        self.username = username
        self.balance = initial_deposit
        self.transactions = []
        self.holdings = {}  # Holds share symbols and quantities
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        """
        Deposits a specified amount of money into the account.
        
        :param amount: The amount of money to deposit.
        """
        self.balance += amount
        self.transactions.append(f"Deposited: ${amount:.2f}")

    def withdraw(self, amount: float) -> None:
        """
        Withdraws a specified amount of money from the account.
        
        :param amount: The amount of money to withdraw.
        :raises ValueError: If the withdrawal exceeds the current balance.
        """
        if self.balance - amount < 0:
            raise ValueError("Cannot withdraw, insufficient balance.")
        self.balance -= amount
        self.transactions.append(f"Withdrew: ${amount:.2f}")

    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Buys a specified quantity of shares of a given symbol.
        
        :param symbol: The stock symbol to buy.
        :param quantity: The number of shares to buy.
        :raises ValueError: If insufficient funds to buy shares.
        """
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if total_cost > self.balance:
            raise ValueError("Cannot buy shares, insufficient funds.")
        
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append(f"Bought: {quantity} shares of {symbol} at ${share_price:.2f} each")

    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Sells a specified quantity of shares of a given symbol.
        
        :param symbol: The stock symbol to sell.
        :param quantity: The number of shares to sell.
        :raises ValueError: If not enough shares to sell.
        """
        if self.holdings.get(symbol, 0) < quantity:
            raise ValueError("Cannot sell shares, insufficient holdings.")
        
        share_price = get_share_price(symbol)
        total_value = share_price * quantity
        
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.balance += total_value
        self.transactions.append(f"Sold: {quantity} shares of {symbol} at ${share_price:.2f} each")

    def calculate_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio.
        
        :return: The total value of the portfolio (balance + value of shares).
        """
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.
        
        :return: The profit or loss from the initial deposit.
        """
        return self.calculate_portfolio_value() - self.initial_deposit

    def report_holdings(self) -> dict:
        """
        Reports the current holdings of the user.
        
        :return: A dictionary of holdings with symbol as keys and quantities as values.
        """
        return self.holdings

    def report_profit_loss(self) -> float:
        """
        Reports the current profit or loss of the user.
        
        :return: The current profit or loss.
        """
        return self.calculate_profit_loss()

    def list_transactions(self) -> list:
        """
        Lists all transactions made by the user.
        
        :return: A list of transaction strings.
        """
        return self.transactions

def get_share_price(symbol: str) -> float:
    """
    Mock function to return fixed prices for certain shares.
    
    :param symbol: The stock symbol.
    :return: The share price.
    """
    prices = {
        "AAPL": 150.00,
        "TSLA": 700.00,
        "GOOGL": 2800.00
    }
    return prices.get(symbol, 0.0)  # Return 0 for unknown symbols