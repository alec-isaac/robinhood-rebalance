import json
import time
import pyotp
import pprint
import config 
import requests
import numpy as np
import pandas as pd
import robin_stocks as rs
import alpaca_trade_api as tradeapi

from decimal import *
from pytz import timezone
from datetime import datetime, timedelta


#! need to adjust code logic to ensure that two factor auth works
# defualt cash weight is .10 (10%) however, the reserve is always going to be set to .025 (2.5%) to ensure cash on hand to place orders
class BaseClass:

    def __init__(self, email, password, mfa_key=None, cash_weight=.10, alpaca_base_url=None, alpaca_key_id=None, alpaca_secret_key=None):
        
        if not isinstance(email, str):
            raise TypeError("Email should be a string.")

        if not isinstance(password, str):
            raise TypeError("Password should be a string.")

        if mfa_key is not None:
            if not isinstance(mfa_key, str):
                raise TypeError("MFA Key should be a string.")

        if not isinstance(cash_weight, float):
            raise TypeError("Cash Weight should be a float.")

        if alpaca_base_url is not None:
            if not isinstance(alpaca_base_url, str):
                raise TypeError("Base URL should be a string.")

        if alpaca_key_id is not None:
            if not isinstance(alpaca_key_id, str):
                raise TypeError("Alpaca Key should be a string.")

        if alpaca_secret_key is not None:
            if not isinstance(alpaca_secret_key, str):
                raise TypeError("Alpaca Secret Key should be a string.")

        self.email = email
        self.password = password
        self.mfa_key = mfa_key
        self.cash_weight = Decimal(cash_weight)
        self.alpaca_base_url = alpaca_base_url
        self.alpaca_key_id = alpaca_key_id
        self.alpaca_secret_key = alpaca_secret_key
        

    def two_factor_auth_code(self):
        
        totp = pyotp.TOTP(self.mfa_key).now()
        print('The Following 6 Digit OTP is your Confirmation Code For Authorized App')
        print("Current OTP:", totp)

    
    # if no alpaca info is provided, this will automatically return True, up to user to ensure that market is open and will be open for the reccomended 30 min rebalance period
    def is_market_open(self):

        try:

            api = tradeapi.REST(
                base_url = self.alpaca_base_url,
                key_id = self.alpaca_key_id,
                secret_key = self.alpaca_secret_key
                )

            nyc = timezone('America/New_York')
            today = datetime.today().astimezone(nyc)
            today_str = datetime.today().astimezone(nyc).strftime('%Y-%m-%d')
            calendar = api.get_calendar(start=today_str, end=today_str)[0]
            market_open = today.replace(
                hour=calendar.open.hour,
                minute=calendar.open.minute,
                second=0
            )
            market_open = market_open.astimezone(nyc)
            market_close = today.replace(
                hour=calendar.close.hour,
                minute=calendar.close.minute,
                second=0
            )
            market_close = market_close.astimezone(nyc)

            current_dt = datetime.today().astimezone(nyc)
            since_market_open = current_dt - market_open
            minutes_since_market_opened = since_market_open.seconds // 60
            hours_since_market_opened = minutes_since_market_opened / 60 

            # Set to less than or equal to 6 hrs to ensure a minimum 30 min trading window for all orders to process
            return hours_since_market_opened <= 6

        except:

            return True


    def load_account_profile(self):
        return rs.profiles.load_account_profile(info=None)


    def load_basic_profile(self):
        return rs.profiles.load_basic_profile(info=None)

    # logs you into your account - session default is set to be on for 2 hrs, default does not store session info - allows you to log into a different account after logging out of yours
    def login_robinhood(self, expires_in=7200, store_session_bool=False):

        if self.mfa_key is None:
            login = rs.login(self.email, self.password, expiresIn=expires_in, scope='internal', by_sms=True, store_session=store_session_bool)
            print(f'Logged in to --> {self.email}')
        else:
            totp  = pyotp.TOTP(self.mfa_key).now()
            login = rs.login(self.email, self.password, expiresIn=expires_in, scope='internal', by_sms=True, store_session=store_session_bool, mfa_code=totp)
            print(f'Logged in to --> {self.email}')


    def logout_robinhood(self):
        rs.authentication.logout()
        print(f'Logged out of --> {self.email}')


    # retrieves all symbols from your robinhood portfolio
    def symbols_list(self):
        return list(rs.account.build_holdings(with_dividends=False))


    # ensures a user's account is eligible for fractionals
    def user_eligible_for_fractionals(self):
        return rs.profiles.load_account_profile(info='eligible_for_fractionals')


    # ensures all symbols in a user's portfolio are eligible for fractional trading
    def symbols_eligible_for_fractionals(self):
        is_eligible = []
        for symbol in self.symbols_list():

            stock_fractional_tradability = rs.stocks.get_instruments_by_symbols(symbol, info='fractional_tradability')
            
            if len(stock_fractional_tradability) == 0:
                is_eligible.append(False)
            elif stock_fractional_tradability[0] == 'position_closing_only':
                is_eligible.append(False)
            elif stock_fractional_tradability[0] == 'untradable':
                is_eligible.append(False)
            else:
                is_eligible.append(True)

        return all(is_eligible) == True

    
    # returns the portfolio (less cash reserved) as the buying power for the rebalance
    def portfolio_value_after_cash_reserved(self):
        portfolio_value = Decimal((rs.account.build_user_profile()['equity']))
        return round(portfolio_value - Decimal(portfolio_value * self.cash_weight), 2)


    # returns the current quantity of each symbol in portfolio
    def quantity_of_shares_per_symbol(self):
        return {
            symbol: round(Decimal(holding_info['quantity']), 6)
            for symbol, holding_info in rs.account.build_holdings(with_dividends=False).items()
            }


    # returns the current equity of each symbol in portfolio
    def equity_of_shares_per_symbol(self):
        return {
            symbol: Decimal(info['equity'])
            for symbol, info in rs.account.build_holdings(with_dividends=False).items()
            }


    # returns the last trade price for each symbol
    def price_quote(self):
        return {
            symbol: Decimal(rs.stocks.get_stock_quote_by_symbol(symbol, info=None)['last_trade_price'])
            for symbol in self.symbols_list()
            }


    # ensures that all transactions below the min drift dollar amount are not processed
    def min_portfolio_drift(self, symbol, quantity, min_drift_amt):
        price_quote = Decimal(rs.stocks.get_stock_quote_by_symbol(symbol, info=None)['last_trade_price'])
        trans_amt = round((quantity * price_quote), 2)

        if trans_amt < min_drift_amt:
            print(f'{symbol} Not Processed - Transaction Amount Lower than Drift Threshold Amount of ${min_drift_amt}')

        return trans_amt >= min_drift_amt

  
    # recursive method to sell fractional shares - as unlike in the APP, Robinhoods orderflow does not always process from the API on the first request
    def place_sell_order(self, symbol, quantity, count=1, completed=False):

        if count <= 5 and not completed: 

            print(f'Starting Sale of {quantity} Shares of {symbol}')
            # stores pre-sale quantity info
            quantity_held_before_sale = self.quantity_of_shares_per_symbol()[symbol]
            # sells a specified amount
            order = rs.orders.order_sell_market(symbol, quantity, timeInForce='gfd', priceType='bid_price', extendedHours=False)
            # allows time for the order to go through
            time.sleep(5)
            
            # stores post-sale quantity info
            # try/except is used to prevent errors from entire positions being closed and then no record of the symbol in your portfolio
            try:
                quantity_now_held = self.quantity_of_shares_per_symbol()[symbol]
            except KeyError:
                quantity_now_held = 0

            if (quantity_held_before_sale - quantity_now_held) == 0:
                print(f'Order to Sell {quantity} Shares of {symbol} Not Processed: Initiating {count} of 5 Attempts to Reprocess')
                self.place_sell_order(symbol, quantity, count+1, False)
            elif quantity_held_before_sale - quantity_now_held != quantity:
                print(f'Order to Sell {quantity} Shares of {symbol} Partially Filled: Initiating {count} of 5 Attempts to Reprocess')
                remaining_qty_to_fill = quantity - (quantity_held_before_sale - quantity_now_held)


                self.place_sell_order(symbol, remaining_qty_to_fill, count+1, False)
            else:
                print(f'Order to Sell {quantity} Shares of {symbol} Processed')
                self.place_sell_order(symbol, quantity, 10, True)

        elif count == 10 and completed:
            print('-------- Onward with the Rebalance --------')

        else:
            print('Unable to Process Sale Order')


    # recursive method to buy fractional shares - as unlike in the APP, Robinhoods orderflow does not always process from the API on the first request
    def place_buy_order(self, symbol, quantity, count=1, completed=False):

        if count <= 5 and not completed:

            print(f'Starting Purchase of {quantity} Shares of {symbol}')
            # stores pre-purchase quantity info
            quantity_held_before_purchase = self.quantity_of_shares_per_symbol()[symbol]
            # buys a specified amount
            order = rs.orders.order_buy_market(symbol, quantity, timeInForce='gfd', priceType='ask_price', extendedHours=False)
            # allows time for the order to go through
            time.sleep(5)
            # stores post-purchase quantity info
            quantity_now_held = self.quantity_of_shares_per_symbol()[symbol]

            if (quantity_held_before_purchase - quantity_now_held) == 0:
                print(f'Order to Purchase {quantity} Shares of {symbol} Not Processed: Initiating {count} of 5 Attempts to Reprocess')
                self.place_buy_order(symbol, quantity, count+1, False)
            elif (quantity_held_before_purchase + quantity) != quantity_now_held:
                print(f'Order to Purchase {quantity} Shares of {symbol} Partially Filled: Initiating {count} of 5 Attempts to Reprocess')
                remaining_qty_to_fill = quantity - (quantity_now_held - quantity_held_before_purchase)
                
                # Ensures you dont try to buy less than $1.1 worth of stock
                if self.min_portfolio_drift(symbol, remaining_qty_to_fill, 1.5):
                    self.place_buy_order(symbol, remaining_qty_to_fill, count+1, False)
                else:
                    print('Remaining Qty Not Filled')
                    self.place_buy_order(symbol, quantity, 10, True)
            else:
                print(f'Order to Purchase {quantity} Shares of {symbol} Processed')
                self.place_buy_order(symbol, quantity, 10, True)
        
        elif count == 10 and completed:
            print('-------- Onward with the Rebalance --------')

        else:
            print('Unable to Process Purchase Order')
        


