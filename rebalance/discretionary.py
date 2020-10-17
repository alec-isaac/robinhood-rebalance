import json
import time
import pyotp
import pprint
import config 
import numpy as np
import pandas as pd
import robin_stocks as rs

from decimal import *

from base import BaseClass


class DiscretionaryWeight(BaseClass):
    
    # returns true if not all weights add to 100%
    def check_discretionary_weights(self, discretionary_weights):
        # print(round(self.cash_weight, 2))
        discretionary_portfolio_weight = Decimal(sum(discretionary_weights.values()))
        return round(discretionary_portfolio_weight, 2) + round(self.cash_weight, 2) == 1


    # returns the total of your discretionary weights - needs to be 1 in order for this to process
    def sum_discretionary_weights(self, discretionary_weights):
        discretionary_portfolio_weight = Decimal(sum(discretionary_weights.values()))
        return (round(discretionary_portfolio_weight, 2) + round(self.cash_weight, 2))
        

    # provides the removed symbols that are not present in your discretionary rebalance
    def compare_symbols(self, discretionary_weights):

        symbols = self.symbols_list()
        removed_symbols = []

        for symbol in symbols:
            if symbol not in discretionary_weights.keys():
                removed_symbols.append(symbol)

        return removed_symbols


    # closes positions not included in discretionary portfolio 
    def close_positions_not_included(self, removed_symbols):

        for symbol in removed_symbols:

            # fetch current quantity 
            quantity = self.quantity_of_shares_per_symbol()[symbol]
            # sell all
            order = self.place_sell_order(symbol, quantity, 1)


    # returns the equity $ to be invested in each symbol - depending on the weight % allocated to it - rounded to nearest penny
    def target_rebalance_equity_amt(self, discretionary_weights):

        rebalance_equity = self.portfolio_value_after_cash_reserved()
        target_equity_allocation = {}

        for symbol, weight in discretionary_weights.items():
            allocated_equity = Decimal(weight) * rebalance_equity
            target_equity_allocation[symbol] = Decimal(allocated_equity)

        return target_equity_allocation


    # returns for each symbol the $ amount required to buy or sell to reach the target decimal % weight allocated to each symbol
    def equity_allocation_difference(self, discretionary_weights):

        rebalance_target_equity_amts = self.target_rebalance_equity_amt(discretionary_weights)
        current_equity_amts = self.equity_of_shares_per_symbol()

        equity_allocation_difference = {}

        for symbol, curr_equity_allocation in current_equity_amts.items():
            for symbol_, target_equity_allocation in rebalance_target_equity_amts.items():
                if symbol == symbol_:
                    # if this is a positive, need to buy $ of share, if negative, sell that amount of shares
                    equity_allocation_difference[symbol] = Decimal((target_equity_allocation - curr_equity_allocation))

        return equity_allocation_difference


    # returns for each symbol the qty amount required to buy or sell to reach the target decimal % weight allocated to each symbol
    def quantity_allocation_difference(self, discretionary_weights):

        equity_allocation_difference = self.equity_allocation_difference(discretionary_weights)
        symbol_price_quote = self.price_quote()

        quantity_allocation_difference = {}

        for symbol, allocation_difference in equity_allocation_difference.items():
            for symbol_, price_quote in symbol_price_quote.items():
                if symbol == symbol_:
                    # if this is a positive, need to buy $ of share, if negative, sell that amount of shares
                    quantity_allocation_difference[symbol] = round(allocation_difference / price_quote, 6)

        return quantity_allocation_difference
   
   
    # rebalance handler
    def rebalance(self, discretionary_weights, min_drift_amt=1.5, min_symbol_equity_amt=5):

        if self.is_market_open():

            print('Market is Open!')

            if not self.check_discretionary_weights(discretionary_weights):
                print(f'Sorry your discretionary weights do not add up to 100%, they add up to {self.sum_discretionary_weights(discretionary_weights) * 100}')
            
            else:

                if min_drift_amt < 1.5:
                    print(f'{min_drift_amt} is below the Min Threshold $ Amount Per Trade of $1.50')
                    print('Min $ Amount Per Trade Set to Mandatory Minimum Default of $1.50')
                    min_drift_amt = 1.5

                print('Rebalance Initiated - Checking User and Portfolio Eligibility for Fractional Trading...')
                if self.user_eligible_for_fractionals() and self.symbols_eligible_for_fractionals():

                    print('User and Portfolio Approved – Starting Rebalance...')

                    removed_symbols = self.compare_symbols(discretionary_weights)

                    print('The Following Are The Removed Symbols That Fell Below Threshold Equity Holding Amount of ${}:'.format(min_symbol_equity_amt), *removed_symbols, sep='\n- ')
                    print('Closing Removed Symbols Positions Now...')
                    closing_positions = self.close_positions_not_included(removed_symbols)

                    print('Calculating Rebalance Purchase and Sale Quantities For Each Symbol...')
                    quantity_allocation = self.quantity_allocation_difference(discretionary_weights)
                    
                    print('Sorting Symbols for Rebalance Process...')
                    # returns an array of tuples - used so that you sell first - keeps investable cash reserves ready to deploy for purchasing
                    sorted_sell_to_buy = sorted(quantity_allocation.items(), key=lambda x: x[1])

                    for symbol, quantity_difference in sorted_sell_to_buy:

                        if quantity_difference >= 0:    
                            if self.min_portfolio_drift(symbol, quantity_difference, min_drift_amt):
                                self.place_buy_order(symbol, quantity_difference, 1)
                        elif quantity_difference < 0:
                            if self.min_portfolio_drift(symbol, -quantity_difference, min_drift_amt):
                                self.place_sell_order(symbol, -quantity_difference, 1)
                        else:
                            return

                    print('Rebalance Completed!')

                else:
                    if not self.user_eligible_for_fractionals():
                        print('Sorry Your Account is Not Eligible For Fractional Trading')
                    else:
                        print('Sorry a Symbol(s) in your Portfolio Are Not Eligible For Fractionals')

        else:
            print('Market is Closed or Within 30 Mins of Closing - Try During Next Open Market Hours')


