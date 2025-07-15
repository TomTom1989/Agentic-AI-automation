import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("test_user", 1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)

    def test_withdraw(self):
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, 700.0)

    def test_withdraw_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(2000.0)

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.0)

    def test_buy_shares(self):
        self.account.buy_shares("AAPL", 3)
        self.assertEqual(self.account.holdings["AAPL"], 3)
        self.assertEqual(self.account.balance, 700.0)

    def test_buy_shares_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 10)

    def test_sell_shares(self):
        self.account.buy_shares("AAPL", 3)
        self.account.sell_shares("AAPL", 1)
        self.assertEqual(self.account.holdings["AAPL"], 2)
        self.assertAlmostEqual(self.account.balance, 850.0, places=2)  # 150 * 1 = 150, 700 + 150 = 850

    def test_sell_shares_insufficient_holdings(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 5)

    def test_total_portfolio_value(self):
        self.account.deposit(100.0)
        self.account.buy_shares("AAPL", 3)
        self.assertAlmostEqual(self.account.total_portfolio_value(), 700.0 + (150.0 * 3), places=2)

    def test_profit_or_loss(self):
        self.account.deposit(100.0)
        self.account.buy_shares("AAPL", 3)
        self.assertAlmostEqual(self.account.profit_or_loss(), (700.0 + (150.0 * 3)) - 1100.0, places=2)

    def test_report_holdings(self):
        self.account.buy_shares("AAPL", 3)
        self.assertEqual(self.account.report_holdings(), {"AAPL": 3})

    def test_report_profit_or_loss(self):
        self.account.deposit(100.0)
        self.account.buy_shares("AAPL", 3)
        self.assertAlmostEqual(self.account.report_profit_or_loss(), (700.0 + (150.0 * 3)) - 1100.0, places=2)

    def test_list_transactions(self):
        self.account.deposit(200.0)
        self.account.withdraw(50.0)
        self.assertIn("Deposited 200.0", self.account.list_transactions())
        self.assertIn("Withdrew 50.0", self.account.list_transactions())

if __name__ == "__main__":
    unittest.main()