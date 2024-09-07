import yfinance as yf
from tabulate import tabulate
from dotenv import load_dotenv
import requests
import os
import json
import logging

########################################################################
# Coinmarketcap API key and URL
load_dotenv()
CMC_API_KEY = os.getenv("CMC_API_KEY")
if not CMC_API_KEY:
    raise ValueError("API Key not found! Please set CMC_API_KEY in your .env file.")
CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# JSON file to store portfolio data
PORTFOLIO_FILE = 'portfolios.json'

########################################################################
class Portfolio:
    def __init__(self, name):
        self._name = name # Attribute 1: portfolio name
        self._stocks = {} # Attribute 2: stocks
        self._crypto = {} # Attribute 3: crypto

    ########################################################################
    # Getter for portfolio name
    @property
    def name(self):
        return self._name

    # Setter for portfolio name
    @name.setter
    def name(self, new_name):
        if not new_name:
            raise ValueError("\nPortfolio name cannot be empty.")
        self._name = new_name

    #########################################################################
    # Getter for stocks
    @property
    def stocks(self):
        return self._stocks

    # Setter for stocks
    @stocks.setter
    def stocks(self, value):
        raise ValueError("\nPlease use add_stock method!")

    #########################################################################
    # Getter for crypto
    @property
    def crypto(self):
        return self._crypto

    # Setter for s
    @crypto.setter
    def crypto(self, value):
        raise ValueError("\nPlease use add_crypto method.")
    #########################################################################

    def get_stock_price(self, ticker):
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")
        return price["Close"].iloc[0]

    def get_crypto_price(self, symbol):
        headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
        params = {
        'symbol': symbol.upper(),
        'convert': 'USD'
        }
        response = requests.get(CMC_URL, headers = headers, params = params)
        price = response.json()
        return price['data'][symbol]['quote']['USD']['price']

########################################################################
# Function to load portfolios from JSON file.
def load_portfolios():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'r') as file:
            portfolios_data = json.load(file)
        portfolios = {}
        for name, data in portfolios_data.items():
            portfolio = Portfolio(name)
            portfolio._stocks = data.get('stocks', {})
            portfolio._crypto = data.get('crypto', {})
            portfolios[name] = portfolio
        return portfolios
    else:
        return {}

# Function to save portfolios to JSON file.
def save_portfolios(portfolios):
    portfolios_data ={}
    for name, portfolio in portfolios.items():
        portfolios_data[name] = {
            'stocks': portfolio.stocks,
            'crypto': portfolio.crypto
        }
    with open(PORTFOLIO_FILE, 'w') as file:
        json.dump(portfolios_data, file, indent=4)

########################################################################
# stock
# Suppress yfinance logs
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

def validate_ticker(ticker):
    # Validate if the ticker symbol exists and get the company name.
    stock = yf.Ticker(ticker)

    try:
        company_name = stock.info['shortName']
        return True, company_name
    except Exception: # If the ticker does not exist
        return False, None

def add_stock(portfolio, ticker, shares, buy_price, confirmation=None):
    # Validate the ticker symbol first.
    is_valid, company_name = validate_ticker(ticker)

    if not is_valid:
        return (f"\nError: ticker symbol '{ticker}' does not exist!")

    if confirmation is None:
        confirmation = input(f"\nTicker '{ticker}' corresponds to '{company_name}'. Are you sure you want to add this stock? (y/n): ").lower()

    if confirmation != 'y':
        return ("\nOperation cancelled.")


    if ticker in portfolio.stocks:
        # Get the current amount of shares and (average) buy price
        old_shares = portfolio.stocks[ticker]['shares']
        old_buy_price = portfolio.stocks[ticker]['buy_price']

        # Calculate the new total shares
        new_total_shares = old_shares + shares

        # Calculate the new weighted average buy price
        new_buy_price = ((old_shares * old_buy_price) + (shares * buy_price)) / new_total_shares

        # Update the stock with the new total shares and new average buy price
        portfolio.stocks[ticker]['shares'] = new_total_shares
        portfolio.stocks[ticker]['buy_price'] = new_buy_price
    else:
        portfolio.stocks[ticker] = {'shares': shares, 'buy_price': buy_price}

    return (f"\nAdded {shares} shares of {ticker} to portfolio '{portfolio.name}' at {buy_price} per share.")

# crypto
def validate_crypto(symbol):
    # Validate if the crypto symbol exists and get its name.
    headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
    params = {
        'symbol': symbol.upper(),
        'convert': 'USD'
    }

    try:
        response = requests.get(CMC_URL, headers=headers, params=params)
        data = response.json()

        # Check if the cryptocurrency symbol exists in the API response
        if symbol.upper() in data['data']:
            crypto_name = data['data'][symbol.upper()]['name']
            return True, crypto_name
        else:
            return False, None
    except Exception: # If the symbol does not exist
        return False, None

def add_crypto(portfolio, symbol, amount, buy_price, confirmation=None):
    # Validate the crypto symbol first.
    is_valid, crypto_name = validate_crypto(symbol)

    if not is_valid:
        return (f"\nError: cryptocurrency symbol '{symbol}' does not exist!")
    if confirmation is None:
        confirmation = input(f"\nSymbol '{symbol}' corresponds to '{crypto_name}'. Are you sure you want to add this cryptocurrency? (y/n): ").lower()

    if confirmation != 'y':
        return ("\nOperation cancelled.")

    if symbol in portfolio.crypto:
        # Get the current amount and (average) buy price
        old_amount = portfolio.crypto[symbol]['amount']
        old_buy_price = portfolio.crypto[symbol]['buy_price']

        # Calculate the new total amount
        new_total_amount = old_amount + amount

        # Calculate the new weighted average buy price
        new_buy_price = ((old_amount * old_buy_price) + (amount * buy_price)) / new_total_amount

        # Update the crypto with the new total amount and new average buy price
        portfolio.crypto[symbol]['amount'] = new_total_amount
        portfolio.crypto[symbol]['buy_price'] = new_buy_price
    else:
        portfolio.crypto[symbol] = {'amount': amount, 'buy_price': buy_price}

    return (f"\nAdded {amount} units of {symbol} ({crypto_name}) to portfolio '{portfolio.name}' at {buy_price} per unit.")

########################################################################
#stock
def sell_stock(portfolio, ticker, shares_to_sell, sell_price):
    # Validate the ticker symbol exists in the portfolio.
    if ticker not in portfolio.stocks:
        return (f"\nError: You do not own any shares of '{ticker}'!")

    current_shares = portfolio.stocks[ticker]['shares']
    avg_buy_price = portfolio.stocks[ticker]['buy_price']

    # Check if enough shares to sell.
    if shares_to_sell > current_shares:
        return (f"\nError: You only own {current_shares} shares of '{ticker}', cannot sell {shares_to_sell}.")

    realised_pnl = (sell_price - avg_buy_price) * shares_to_sell

    if 'realised_pnl' not in portfolio.stocks[ticker]:
        portfolio.stocks[ticker]['realised_pnl'] = 0

    portfolio.stocks[ticker]['realised_pnl'] += realised_pnl

    new_share_count = current_shares - shares_to_sell
    if new_share_count > 0:
        portfolio.stocks[ticker]['shares'] = new_share_count
        return (f"\nSold {shares_to_sell} shares of {ticker}. Realised PnL: ${realised_pnl:,.2f}. You now own {new_share_count:,.2f} shares.")
    else:
        # Remove the stock if the new share count is zero
        del portfolio.stocks[ticker]
        return (f"\nSold all shares of {ticker}. Realised PnL: ${realised_pnl:,.2f}. You no longer own any shares of {ticker}.")

#crypto
def sell_crypto(portfolio, symbol, amount_to_sell, sell_price):
    # Validate the crypto symbol exists in the portfolio.
    if symbol not in portfolio.crypto:
        return (f"\nError: You do not own any units of '{symbol}'!")

    current_amount = portfolio.crypto[symbol]['amount']
    avg_buy_price = portfolio.crypto[symbol]['buy_price']

    # Check if enough units to sell.
    if amount_to_sell > current_amount:
        return (f"\nError: You only own {current_amount} units of '{symbol}', cannot sell {amount_to_sell}.")

    realised_pnl = (sell_price - avg_buy_price) * amount_to_sell

    if 'realised_pnl' not in portfolio.crypto[symbol]:
        portfolio.crypto[symbol]['realised_pnl'] = 0

    portfolio.crypto[symbol]['realised_pnl'] += realised_pnl

    new_amount = current_amount - amount_to_sell
    if new_amount > 0:
        portfolio.crypto[symbol]['amount'] = new_amount
        return (f"\nSold {amount_to_sell} units of {symbol}. Realised PnL: ${realised_pnl:,.2f}. You now own {new_amount:,.2f} units.")
    else:
        # Remove the crypto if the new amount is zero
        del portfolio.crypto[symbol]
        return (f"\nSold all units of {symbol}. Realised PnL: ${realised_pnl:,.2f}. You no longer own any shares of {symbol}.")

########################################################################
# Calculate total portfolio value by fetching real-time prices.
def display_portfolio(portfolio):
    # Display portfolio holdings in a table using tabulate.

    # Create a list to store table data
    table = []
    total_value = 0
    total_realised_pnl = 0
    total_unrealised_pnl = 0

    # Iterate over stocks and cryptos in the portfolio
    # stock value
    for ticker, data in portfolio.stocks.items():
        stock_price = portfolio.get_stock_price(ticker)
        total_value += data['shares'] * stock_price

        unrealised_pnl = (stock_price - data['buy_price'])* data['shares']
        unrealised_pnl_percentage = (unrealised_pnl / (data['buy_price'] * data['shares'])) * 100
        total_unrealised_pnl += unrealised_pnl

        realised_pnl = data.get('realised_pnl', 0)
        total_realised_pnl += realised_pnl

        table.append([
            ticker,
            f"{data['shares']:,.2f} shares",
            f"${stock_price:,.2f} per share",
            f"${data['shares'] * stock_price:,.2f}",
            f"${data['buy_price']:,.2f}",
            f"${unrealised_pnl:,.2f}",
            f"{unrealised_pnl_percentage:.2f} %"
        ])

    # cryptocurrency value
    for symbol, data in portfolio.crypto.items():
        crypto_price = portfolio.get_crypto_price(symbol)
        total_value += data['amount'] * crypto_price

        unrealised_pnl = (crypto_price - data['buy_price'])* data['amount']
        unrealised_pnl_percentage = (unrealised_pnl / (data['buy_price'] * data['amount'])) * 100
        total_unrealised_pnl += unrealised_pnl

        realised_pnl = data.get('realised_pnl', 0)
        total_realised_pnl += realised_pnl

        table.append([
            symbol,
            f"{data['amount']:,.2f} amount",
            f"${crypto_price:,.2f} per unit",
            f"${data['amount'] * crypto_price:,.2f}",
            f"${data['buy_price']:,.2f}",
            f"${unrealised_pnl:,.2f}",
            f"{unrealised_pnl_percentage:.2f} %"
        ])

    # Headers for table
    headers = [
        "Asset",
        "Quantity",
        "Current Price",
        "Total Value",
        "Avg Buy Price",
        "Unrealised PnL",
        "Unrealised PnL (%)"
        ]

    print("\n" + tabulate(table, headers, tablefmt="grid"))

    print(f"Total portfolio value for '{portfolio.name}': ${total_value:,.2f}")
    print(f"Total unrealised gain/loss for '{portfolio.name}': ${total_unrealised_pnl:,.2f}")
    print(f"Total realised gain/loss for '{portfolio.name}': ${total_realised_pnl:,.2f}\n")

    return total_value

########################################################################
def print_boxed_message(message):
    # This is to determine box length
    message_length = len(message)

    # Top and Bottom border
    border = "+" + "*" * (message_length + 2) + "+"

    # Left and Right border with message
    content = f"{message}"

    return border, content

########################################################################
def main():
    portfolios = load_portfolios() # Load portfolios when run.

    while True:
        print("\n* CryptoStock Tracker *")
        print("-----------------------------------------------------------------------------------------")
        print("Available portfolios:")
        for name in portfolios:
            print(f"- {name}")
        print("\nMenu:")
        print("1. Create a new portfolio")
        print("2. Add Stock to a portfolio")
        print("3. Add Crypto to a portfolio")
        print("4. Sell Stock from a portfolio")
        print("5. Sell Crypto from a portfolio")
        print("6. View portfolio value")
        print("7. Rename a portfolio")
        print("8. Exit")

        try:
            choice = int(input("\nEnter your choice in number: ").strip())
        except Exception:
                border, content = print_boxed_message("Invalid input. Please enter a number.")
                print("\n"+ border)
                print(content)
                print(border)
                continue

        if choice == 1:
            portfolio_name = input("\nEnter desired portfolio name: ")
            if portfolio_name in portfolios:
                print(f"\nPortfolio '{portfolio_name}' already exists.")
            else:
                portfolios[portfolio_name] = Portfolio(portfolio_name) # Creating an instance from the class Portfolio
                print(f"\nPortfolio '{portfolio_name}' created.")

        elif choice == 2:
            portfolio_name = input("\nEnter the portfolio name: ")
            if portfolio_name in portfolios:
                display_portfolio(portfolios[portfolio_name])
                ticker = input("Enter the stock ticker to buy (e.g., AAPL): ").upper()
                while True:
                    try:
                        shares = float(input("Enter the number of shares: "))
                        if shares <= 0:
                            raise ValueError("Number of shares must be greater than 0")
                        buy_price = float(input("Enter the buy price per share in USD: "))
                        if buy_price <= 0:
                            raise ValueError("Buy price must be greater than 0")
                        break
                    except ValueError as error:
                        print(f"Invalid input: {error}. Please try again.")
                border, content = print_boxed_message(add_stock(portfolios[portfolio_name], ticker, shares, buy_price))
                print("\n"+ border)
                print(content)
                print(border)
                display_portfolio(portfolios[portfolio_name])
            else:
                print(f"\nPortfolio '{portfolio_name}' does not exist.")

        elif choice == 3:
            portfolio_name = input("\nEnter the portfolio name: ")
            if portfolio_name in portfolios:
                display_portfolio(portfolios[portfolio_name])
                symbol = input("Enter the cryptocurrency symbol to buy (e.g., BTC): ").upper()
                while True:
                    try:
                        amount = float(input("Enter the number of cryptocurrency units: "))
                        if amount <= 0:
                            raise ValueError("Amount must be greater than 0")
                        buy_price = float(input("Enter the buy price per unit in USD: "))
                        if buy_price <= 0:
                            raise ValueError("Buy price must be greater than 0")
                        break
                    except ValueError as error:
                        print(f"Invalid input: {error}. Please try again.")
                border, content = print_boxed_message(add_crypto(portfolios[portfolio_name], symbol, amount, buy_price))
                print("\n"+ border)
                print(content)
                print(border)
                display_portfolio(portfolios[portfolio_name])
            else:
                print(f"\nPortfolio '{portfolio_name}' does not exist.")

        elif choice == 4:
            portfolio_name = input("\nEnter the portfolio name: ")
            if portfolio_name in portfolios:
                display_portfolio(portfolios[portfolio_name])
                ticker = input("Enter the stock ticker to sell(e.g., AAPL): ").upper()
                while True:
                    try:
                        shares_to_sell = float(input("Enter the number of shares: "))
                        if shares_to_sell <= 0:
                            raise ValueError("Number of shares to sell must be greater than 0")
                        sell_price = float(input("Enter the sell price per share in USD: "))
                        if sell_price < 0:
                            raise ValueError("Sell price must be greater than 0")
                        break
                    except ValueError as error:
                            print(f"Invalid input: {error}. Please try again.")
                border, content = print_boxed_message(sell_stock(portfolios[portfolio_name], ticker, shares_to_sell, sell_price))
                print("\n"+ border)
                print(content)
                print(border)
                display_portfolio(portfolios[portfolio_name])
            else:
                print(f"\nPortfolio '{portfolio_name}' does not exist.")

        elif choice == 5:
            portfolio_name = input("\nEnter the portfolio name: ")
            if portfolio_name in portfolios:
                display_portfolio(portfolios[portfolio_name])
                symbol = input("Enter the cryptocurrency symbol to sell (e.g., BTC): ").upper()
                while True:
                    try:
                        amount_to_sell = float(input("Enter the number of cryptocurrency units: "))
                        if amount_to_sell <= 0:
                            raise ValueError("Amount to sell must be greater than 0")
                        sell_price = float(input("Enter the sell price per share in USD: "))
                        if sell_price < 0:
                            raise ValueError("Sell price must be greater than 0")
                        break
                    except ValueError as error:
                            print(f"Invalid input: {error}. Please try again.")
                border, content = print_boxed_message(sell_crypto(portfolios[portfolio_name], symbol, amount_to_sell, sell_price))
                print("\n"+ border)
                print(content)
                print(border)
                display_portfolio(portfolios[portfolio_name])
            else:
                print(f"\nPortfolio '{portfolio_name}' does not exist.")

        elif choice == 6:
            portfolio_name = input("\nEnter the portfolio name: ")
            if portfolio_name in portfolios:
                display_portfolio(portfolios[portfolio_name])
            else:
                print(f"\nPortfolio '{portfolio_name}' does not exist.")

        elif choice == 7:
            old_name = input("\nEnter the portfolio name: ")
            if old_name in portfolios:
                new_name = input("Enter the new portfolio name: ")
                if not new_name:
                    print("\nPortfolio name cannot be empty.")
                elif new_name in portfolios:
                    print(f"\nA portfolio with the name '{new_name}' already exists.")
                else:
                    portfolios[new_name] = portfolios.pop(old_name)
                    portfolios[new_name].name = new_name
                    print(f"\nPortfolio '{old_name}' renamed to '{new_name}'.")
            else:
                print(f"\nPortfolio '{old_name}' does not exist.")

        elif choice == 8:
            save_portfolios(portfolios) # Save portfolios then exit.
            print("\nPortfolios successfully saved. Exiting Portfolio Manager.")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
