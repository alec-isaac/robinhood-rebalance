import config # adjust path as necessary or use .env

from equal import EqualWeight
from market import MarketWeight
from discretionary import DiscretionaryWeight

# Equal Weight Examples

''' First Example
-----------------------------------------------------------------------------------------------------------------------
Uncomment the below code to run an EqualWeightRebalance - No Authorized App - No Alpaca - 25% cash reserved
'''


# portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, None, .25)
# portfolio_rebalance.login_robinhood()
# portfolio_rebalance.rebalance()
# portfolio_rebalance.logout_robinhood()

'''
-----------------------------------------------------------------------------------------------------------------------
'''




''' Second Example
-----------------------------------------------------------------------------------------------------------------------
Uncomment the below code to run an EqualWeightRebalance - No Authorized App - Alpaca Info Included - 25% cash reserved
'''

# portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, None, .25, config.ALPACA_BASE_URL, config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
# portfolio_rebalance.login_robinhood()
# portfolio_rebalance.rebalance()
# portfolio_rebalance.logout_robinhood()

'''
-----------------------------------------------------------------------------------------------------------------------
'''




''' Third Example
-----------------------------------------------------------------------------------------------------------------------
Uncomment the below code (in order instructed) to run an EqualWeightRebalance - Authorized App - Alpaca Info Included - 25% cash reserved
Two Steps Involved With Authorized App - See README login info for further help.
'''

'''
First Step - Retrieve OTP 
(uncomment below code, make sure Step Two Code Remains Commented)
'''

# portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, config.ROBIN_MFA_KEY, .25, config.ALPACA_BASE_URL, config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
# portfolio_rebalance.two_factor_auth_code()

'''
Second Step - After Authorizing the App via Robinhood w/ above OTP 
(uncomment below code, make sure Step One Code is Commented)
'''

# portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, config.ROBIN_MFA_KEY, .25, config.ALPACA_BASE_URL, config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
# portfolio_rebalance.login_robinhood()
# portfolio_rebalance.rebalance()
# portfolio_rebalance.logout_robinhood()

'''
-----------------------------------------------------------------------------------------------------------------------
'''