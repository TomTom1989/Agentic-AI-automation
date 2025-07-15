import gradio as gr
from accounts import Account, get_share_price

account = None

def create_account(username, initial_deposit):
    global account
    account = Account(username, float(initial_deposit))
    return f"Account created for {username} with initial deposit of ${initial_deposit:.2f}"

def deposit(amount):
    if account:
        account.deposit(float(amount))
        return f"Deposited: ${amount:.2f}. New balance: ${account.balance:.2f}"
    return "No account found."

def withdraw(amount):
    if account:
        try:
            account.withdraw(float(amount))
            return f"Withdrew: ${amount:.2f}. New balance: ${account.balance:.2f}"
        except ValueError as e:
            return str(e)
    return "No account found."

def buy_shares(symbol, quantity):
    if account:
        try:
            account.buy_shares(symbol, int(quantity))
            return f"Bought: {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
        except ValueError as e:
            return str(e)
    return "No account found."

def sell_shares(symbol, quantity):
    if account:
        try:
            account.sell_shares(symbol, int(quantity))
            return f"Sold: {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
        except ValueError as e:
            return str(e)
    return "No account found."

def portfolio_value():
    if account:
        return f"Total portfolio value: ${account.calculate_portfolio_value():.2f}"
    return "No account found."

def profit_loss():
    if account:
        return f"Profit/Loss: ${account.calculate_profit_loss():.2f}"
    return "No account found."

def report_holdings():
    if account:
        holdings = account.report_holdings()
        return f"Current holdings: {holdings}"
    return "No account found."

def list_transactions():
    if account:
        transactions = account.list_transactions()
        return f"Transactions: {transactions}"
    return "No account found."

with gr.Blocks() as demo:
    gr.Markdown("### Trading Account Management System")
    username = gr.Textbox(label="Username")
    initial_deposit = gr.Number(label="Initial Deposit")
    gr.Button("Create Account").click(create_account, inputs=[username, initial_deposit], outputs="text")

    deposit_amount = gr.Number(label="Deposit Amount")
    gr.Button("Deposit").click(deposit, inputs=deposit_amount, outputs="text")

    withdraw_amount = gr.Number(label="Withdraw Amount")
    gr.Button("Withdraw").click(withdraw, inputs=withdraw_amount, outputs="text")

    share_symbol = gr.Textbox(label="Share Symbol (e.g., AAPL)")
    buy_quantity = gr.Number(label="Buy Quantity")
    gr.Button("Buy Shares").click(buy_shares, inputs=[share_symbol, buy_quantity], outputs="text")

    sell_quantity = gr.Number(label="Sell Quantity")
    gr.Button("Sell Shares").click(sell_shares, inputs=[share_symbol, sell_quantity], outputs="text")

    gr.Button("Portfolio Value").click(portfolio_value, outputs="text")
    gr.Button("Profit/Loss").click(profit_loss, outputs="text")
    gr.Button("Report Holdings").click(report_holdings, outputs="text")
    gr.Button("List Transactions").click(list_transactions, outputs="text")

demo.launch()