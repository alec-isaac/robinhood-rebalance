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


class MarketWeight(BaseClass):

    # returns the mkt cap for a company if it is available on robinhood
    def get_mkt_caps(self, symbols_list):

        mkt_caps = {}
    
        for symbol in symbols_list:
            if rs.stocks.get_fundamentals(symbol, info='market_cap')[0] is None:
                mkt_caps[symbol] = 0.0
            else:
                mkt_caps[symbol] = float(rs.stocks.get_fundamentals(symbol, info='market_cap')[0])
                
        return mkt_caps

    # returns the mkt cap weight %s for each company using their mkt caps from above
    def get_target_mkt_weight(self, symbols_list, mkt_caps_dict):

        mkt_caps = []
        target_mkt_weight = {}

        for symbol, mkt_cap in mkt_caps_dict.items():
            mkt_caps.append(mkt_cap)

        mkt_cap_weights = mkt_caps/np.sum(mkt_caps)

        i = 0
        while i < len(symbols_list):
            symbol = symbols_list[i]
            mkt_cap_weight = mkt_cap_weights[i]
            target_mkt_weight[symbol] = Decimal(mkt_cap_weight)
            i += 1

        return target_mkt_weight
    
    # returns the equity $ to be invested in each symbol - depending on the weight % allocated to it by market cap- rounded to nearest penny
    def target_mkt_rebalance_equity_amt(self, investable_equity, mkt_cap_weights):

        rebalance_equity = investable_equity
        symbol_target_weights = mkt_cap_weights

        target_equity_allocation = {}

        for symbol, weight in symbol_target_weights.items():
            allocated_equity = weight * rebalance_equity
            target_equity_allocation[symbol] = allocated_equity

        return target_equity_allocation


    # returns for each symbol the $ amount required to buy or sell to reach the target decimal % weight allocated to each symbol
    def adj_equity_allocation_difference(self, adjusted_pre_processed_equity_amts):

        current_equity_amts = self.equity_of_shares_per_symbol()

        adjusted_equity_allocation_difference = {}

        for symbol, curr_equity_allocation in current_equity_amts.items():
            for symbol_, target_equity_allocation in adjusted_pre_processed_equity_amts:
                if symbol == symbol_:
                    # if this is a positive, need to buy $ of share, if negative, sell that amount of shares
                    adjusted_equity_allocation_difference[symbol] = (target_equity_allocation - curr_equity_allocation)

        return adjusted_equity_allocation_difference


    # returns for each symbol the quantity required to buy or sell to reach the target decimal % weight allocated to each symbol
    # if it is negative, means you have to buy shares, if it is positive you should sell them 
    def adj_quantity_allocation_difference(self, adjusted_pre_processed_equity_amts):

        equity_allocation_difference = self.adj_equity_allocation_difference(adjusted_pre_processed_equity_amts)
        symbol_price_quote = self.price_quote()

        adjusted_quantity_allocation_difference = {}

        for symbol, allocation_difference in equity_allocation_difference.items():
            for symbol_, price_quote in symbol_price_quote.items():
                if symbol == symbol_:
                    # if this is a positive, need to buy $ of share, if negative, sell that amount of shares
                    adjusted_quantity_allocation_difference[symbol] = round(allocation_difference / price_quote, 6)

        return adjusted_quantity_allocation_difference


    def close_positions_below_threshold(self, removed_symbols, min_symbol_equity_amt):

        # loop through symbols in removed symbols
        for symbol in removed_symbols:

            # fetch current quantity 
            quantity = self.quantity_of_shares_per_symbol()[symbol]
            # sell all
            order = self.place_sell_order(symbol, quantity, 1)


    # recursive function that updates the equity/qty amounts of each symbol to buy as others are dropped from the portfolio (because they dont reach the threshold)
    def mkt_cap_rebalance_prestep(self, min_symbol_equity_amt, symbols_list_=None, outer_trigger=True, inner_trigger=True, removed_symbols = [], mkt_equity_allocation=None):

        # will run on the first call
        if outer_trigger:

            symbols_ = self.symbols_list()

            equity_allocation = self.target_mkt_rebalance_equity_amt(self.portfolio_value_after_cash_reserved(
            ), self.get_target_mkt_weight(symbols_, self.get_mkt_caps(symbols_)))

            sorted_equity_allocation = sorted(equity_allocation.items(), key=lambda x: x[1])

        # runs on all other calls
        else:

            symbols_ = symbols_list_

            equity_allocation = self.target_mkt_rebalance_equity_amt(self.portfolio_value_after_cash_reserved(
            ), self.get_target_mkt_weight(symbols_, self.get_mkt_caps(symbols_)))

            sorted_equity_allocation = sorted(equity_allocation.items(), key=lambda x: x[1])

        for symbol, equity_amt in sorted_equity_allocation:

            while inner_trigger:
                
                if equity_amt < min_symbol_equity_amt:
                    symbols_.remove(symbol)
                    removed_symbols.append(symbol)
                    return self.mkt_cap_rebalance_prestep(min_symbol_equity_amt, symbols_, False, True, removed_symbols, mkt_equity_allocation)
                else:
                    mkt_equity_allocation = sorted_equity_allocation
                    return self.mkt_cap_rebalance_prestep(min_symbol_equity_amt, symbols_, False, False, removed_symbols, mkt_equity_allocation)

        return (removed_symbols, mkt_equity_allocation)


    # rebalance handler
    def rebalance(self, min_drift_amt=1.5, min_symbol_equity_amt=5, trial_run=False):

        if self.is_market_open():

            print('Market is Open!')

            if min_drift_amt < 1.5:
                print(f'{min_drift_amt} is below the Min Threshold $ Amount Per Trade of $1.50')
                print('Min $ Amount Per Trade Set to Mandatory Minimum Default of $1.50')
                min_drift_amt = 1.5
                
            if min_symbol_equity_amt < 2.5:
                print(f'{min_symbol_equity_amt} is below the Min Threshold $ Amount Per Holding of $2.50')
                print('Min $ Amount Per Holding Set to Mandatory Minimum Default of $2.50')
                min_symbol_equity_amt = 2.5

            print('Rebalance Initiated - Checking User and Portfolio Eligibility for Fractional Trading...')
            if self.user_eligible_for_fractionals() and self.symbols_eligible_for_fractionals():

                print('User and Portfolio Approved – Starting Rebalance...')
                print('Discovering Which Symbols To Remove Based on Mkt Cap Thresholds...')
                removed_symbols, mkt_equity_allocation = self.mkt_cap_rebalance_prestep(min_symbol_equity_amt)
                
                print('The Following Are The Removed Symbols That Fell Below Threshold Equity Holding Amount of ${}:'.format(min_symbol_equity_amt), *removed_symbols, sep='\n- ')
                print('Closing Removed Symbols Positions Now...')
                closing_positions = self.close_positions_below_threshold(removed_symbols, min_symbol_equity_amt)

                print('Calculating Rebalance Purchase and Sale Quantities For Each Symbol...')
                quantity_allocation = self.adj_quantity_allocation_difference(mkt_equity_allocation)

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



