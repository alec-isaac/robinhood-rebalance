###### README.md

<p align='center'><b>Robinhood Rebalance</b></p>

<p align="center">
  <img width="600" height="200" src="https://i.ibb.co/hyqHtdY/Dilbert.jpg">
</p>

<p align='center'><b>An Investing Tool to Rebalance your Portfolio or Create your own ETFs utilizing Robinhood Fractional Trading</b></p>

# Welcome to Robinhood Rebalance

## tl;dr

Robinhood Rebalance requests your Robinhood Portfolio, ensures you are eligible for fractional trading (and that all of your stocks are eligible for fractional trading) and then rebalances it based on your desire weights, i.e., EqualWeight, MarketWeight, or DiscretionaryWeight. 

1. Clone the Repository:
   
   ```python
   # terminal

   >>> git clone https://github.com/alec-isaac/robinhood-rebalance.git
   ```
   
2. Create a config.py or .env file to store required private info:
   
   ```python
    # config.py or .env
    
    ROBIN_EMAIL = "Your Associated Email Here"
    ROBIN_PASS = "Your Associated Password Here"
    ROBIN_MFA_KEY = "Your Associated MFA Key Here" #(if 2FA enabled)
    
    # Alpaca info is only used to ensure that the market is open and at least thirty minutes remain until market closes
    # If you do not not have an alpaca account and do not enter this info, the rebalance will still run but it is up to you to ensure the market is open before running and... 
    # ... that you have the reccomended 30 mins to run the full rebalance (for a portfolio of 30+ shares - mileage may vary)
    
    ALPACA_BASE_URL = "Alpaca's Base URL Here" #(paper account works fine, 'https://paper-api.alpaca.markets')
    ALPACA_KEY_ID = "Your Alpaca Key ID Here"
    ALPACA_SECRET_KEY = "Your Alpaca Secret Key Here"
    ```

3. Create & activate venv 

   ```python
   #terminal
   
   >>> python3 -m venv venv
   >>> source venv/bin/activate
   ```
   
4. Install Required Packages

   ```python
   #terminal

   >>> pip install -r requirements.txt
   ```
   
5. In run_rebalance.py input your Robinhood and/or Alpaca Info and Desired Cash Allocation:

    ##### Equal Weight Rebalance - No Authorized App Enabled - Alpaca Account Info Not Included
   
   ```python
   #run_rebalance.py
   
    portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, None, .1)
    portfolio_rebalance.login_robinhood() #please see login information below to better understand prompts
    portfolio_rebalance.rebalance()
    ```
    
6. In terminal:

   ```python
    #terminal 

   # after cd into rebalance folder
    >>> python run_rebalance.py
    ```
    
 ## Table of Contents
 
 * [Introduction](#introduction)
 * [Rebalance Methodology](#rebalance-methodology)
    * [Summary](#summary)
    * [Equal Weight](#equal-weight)
    * [Market Weight](#market-weight)
    * [Discretionary Weight](#discretionary-weight)
    * [Additional Resources](#additional-resources)
 * [Installation](#installation)
 * [Logging In](#logging-in)
 * [Examples](#examples)
    * [Equal Weight Rebalance](#equal-weight-rebalance)
    * [Market Weight Rebalance](#market-weight-rebalance)
    * [Discretionary Weight Rebalance](#discretionary-weight-rebalance)
 * [Future Updates](#future-updates)
 * [License](#license)
 * [Credits](#credits)
 * [Disclaimer](#disclaimer)
 
## Introduction <a name="introduction"></a>
 
 This package was designed to help Robinhood Users rebalance their portfolios or utilize Robinhood's Fractionals to build their own ETFs. 

## Rebalance Methodology <a name="rebalance-methodology"></a>
 
##### Summary <a name="summary"></a>

Rebalancing your portfolio on a set basis allows you to maintain your established asset allocation amongst equities. Rebalancing provides a seemless oppurtunity to trim back your winners while simultaneously dollar cost averaging your poorer performing assets, ultimately smoothing your returns in the long run.

Additionally, this rebalance package allows you to build your own ETFs by helping you maintain proper allocation to the stocks you curate. 

Financial literature often recommends that you rebalance on a quarterly basis, however, this timing decision is entirely up to your financial goals and current tax position. 

##### Equal Weight <a name="equal-weight"></a>

Equal Weight Rebalancing is typically identified as value based. This rebalance method will ultimately result in you trimming down winning positions and dollar cost averaging out of favor positions. The tradeoff being that equal weight doesn't allow for you to let your "winners run."

[Note that over the last 10 years, the smallest 450+ stocks in the S&P 500 Equal Weight Index not only outperformed the same stocks in the cap-weighted S&P 500, they beat the entire S&P 500 Index's return by 17%.](https://www.invesco.com/us/financial-products/etfs/strategies/equal-weight-investing?audienceType=Investor)

##### Market Weight <a name="market-weight"></a>

Unlike an Equal Weight Rebalance, Market Weight rebalancing is identified as momentum based. As the stock increases or decreases in price (market cap) each rebalance will allocate more or less of your funds into that position. 

* [Advantages & Disadvantages of Market Cap Weighting Holdings](https://www.benefitscanada.com/investments/other-investments/overcoming-the-flaws-of-a-market-capitalization-weighted-index-21902)

##### Discretionary Weight <a name="discretionary-weight"></a>

Discretionary Investing is a dealer's choice based rebalance. One picks both the stock and how much of their portfolio they would like to allocate towards it. Perfect for establishing and maintaining 60/40 portfolios or stacking weight towards stocks which you believe are going to outperform, while including other holdings to diversify. 

##### Additional Resources <a name="additional-resources"></a>

A well articulated Podcast by Corey Hoffstein [Rebalance Timing and Luck](https://flirtingwithmodels.libsyn.com/corey-hoffstein-rebalance-timing-luck-s2e11)

* This Podcast explores the innerworkings of rebalance timing and the performance repercussions resulting in the time and manner in which you rebalance.

For value investors go get your Veggies with the [The Acquirers Multiple](https://podcasts.apple.com/us/podcast/the-acquirers-podcast/id1454112457)

* Podcast covers all things deep value and every Thursday provides an entertaining Value After Hours podcast hosted by Tobias Carlisle, Bill Brewster, and Jake Taylor.

For those running trend strategies check out [Top Traders Unplugged](https://podcasts.apple.com/us/podcast/top-traders-unplugged/id888420325)

* Niels Kaastrup-Larsen does an excellent job delivering both quant strategies and enganging conversations with excellent guests.

For all things Macro check out [Macrovoices](https://podcasts.apple.com/us/podcast/macro-voices/id1079172742)

* Weekly market commentary by Hedge Fund Manager Erik Townsend and interviews with the brightest minds in the world of finance and macroeconomics.
 
## Installation <a name="installation"></a>

1. Clone the Repository:
   
   ```python
   # terminal

   >>> git clone https://github.com/alec-isaac/robinhood_rebalance.git
   ```
   
2. Create a config.py or .env file to store required private info:
   
   ```python
    # config.py or .env
    
    ROBIN_EMAIL = "Your Associated Email Here"
    ROBIN_PASS = "Your Associated Password Here"
    ROBIN_MFA_KEY = "Your Associated MFA Key Here" #(if 2FA enabled)
    
    # Alpaca info is only used to ensure that the market is open and at least thirty minutes remain until market closes
    # If you do not not have an alpaca account and do not enter this info, the rebalance will still run but it is up to you to ensure the market is open before running and... 
    # ... that you have the reccomended 30 mins to run the full rebalance (for a portfolio of 30+ shares - mileage may vary)
    
    ALPACA_BASE_URL = "Alpaca's Base URL Here" #(paper account works fine, 'https://paper-api.alpaca.markets')
    ALPACA_KEY_ID = "Your Alpaca Key ID Here"
    ALPACA_SECRET_KEY = "Your Alpaca Secret Key Here"
    ```

3. Create & activate venv 

   ```python
   #terminal

   >>> python3 -m venv venv
   >>> source venv/bin/activate
   ```
   
4. Install Required Packages

   ```python
   #terminal

   >>> pip install -r requirements.txt
   ```

## Logging In <a name="logging-in"></a>

##### Checking to See if Two-Factor Authentication (2FA) is Enabled

Log in to Robinhood.com or on your Mobile App... 

Account --> Settings --> Security --> Two-Factor Authentication (off/on)

##### No 2FA Enabled

* If 2FA is not enabled on your Robinhood account, you only need your username and password to log in. Then after running 'python run_rebalance.py' in the terminal you will be prompted with...

Enter Robinhood code for validation: <'Enter Your SMS 6 Digit Code Here'>

* After entering the SMS Code the Rebalance Process will Initiate.

##### 2FA SMS ENABLED

* If 2FA SMS is Enabled, you will still only be required to fill in your username and password to log in. Then after running 'python run_rebalance.py' in the terminal you will be prompted with...

Please type in the MFA code: <'Enter Your SMS 6 Digit MFA Code Here'>

* After entering the SMS MFA Code the Rebalance Process will Initiate.

##### 2FA Authorized App Enabled

* If 2FA Authorized App is Enabled or you wish to Enable it there are additional steps required before you can begin your rebalance. 

* After your session has expired or after you log out you will need to repeat the foregoing steps to regenerate an OTP Code.

#### Steps:

##### #1. Enable 2FA Authorized App 

  * Log in to Robinhood.com or on your Mobile App... 

  * Account --> Settings --> Security --> Two-Factor Authentication (off/on)

  * Enabled 2FA and Choose 'Authentication App' --> Next

  * Click 'Can't scan it?' --> See MFA Key that resembles 'ERGZS34DV7QZK8AB'

  * Grab the MFA Key and Paste it in to your .config or .env file

* Hit Next --> Prompt to enter the 6-digit code you see in the Robinhood app...

##### #2. Retrieve the OTP Code 

   ```python
   #run_rebalance.py

   portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, config.ROBIN_MFA_KEY, .3)
   portfolio_rebalance.two_factor_auth_code() #In terminal this will print out 'Current OTP: <6 Digit Num Here>
   ``` 

  * Take your OTP code and paste it back into the Robinhood Screen at the end of Step #1... you are now authorized to login and Initiate the Rebalance.

##### #3. Comment out the above print outs and your run_rebalance.py file should look like this

   ```python
   #run_rebalance.py

   # portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, config.ROBIN_MFA_KEY, .3)
   # portfolio_rebalance.two_factor_auth_code() 

   portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, config.ROBIN_MFA_KEY, .3)
   portfolio_rebalance.login_robinhood()
   portfolio_rebalance.rebalance()
   portfolio_rebalance.logout_robinhood()

   ```

##### #4. Run run_rebalance.py

   ```python
   #terminal

   # after cd into rebalance folder
   >>> python run_rebalance.py
   ```

##### Configuring Login Permissions

The method login_robinhood contains the following default arguments:

1. expires_in=7200 <-- Two Hours Until Expiration

2. store_session_bool=False <-- Allows a different users account to be logged in with after logging out of prior user

* If only one user, switch store_session_bool to false and increase the expiration timing (in seconds) to reduce the number of log ins.

## Examples <a name="examples"></a>

#### Caveats: 

* Rebalance will only work if you are approved for fractionals and all shares in your portfolio are approved for fractional trading. [Which Shares Are Approved For Fractionals](https://robinhood.com/us/en/support/articles/fractional-shares/)

* Only run the rebalance during market hours: the rebalance will techinically "run" after hours, but will not properly work. You will get all types of queued orders, however, because you cannot sell after hours, your buying power will be ineffective.

* The rebalance will always sell shares to increase buying power before acquiring more. 
 
##### Equal Weight Rebalance <a name="equal-weight-rebalance"></a>

The MarketWeight method takes (1) optional arugments:

* First - Minimum Drift Amount: By default this amount is set to the mandatory minimum of $1.50 - this is because Robinhood will not allow you to execute a non-position closing trade that is below $1 in total value and the additional .50 cents provides a margin of safety to ensure your trade executes even with volatile market price swings. 

However, you may set this Minimum Drift Amount $ higher than a $1.50. For example: setting the Minimum Drift Amount $ to $10 would mean that any rebalancing buy or sell transaction that falls below $10 in value would not be executed, essentially you are allowing the rebalance to drift within a $10 +/- collar range.

In run_rebalance.py input your Robinhood and/or Alpaca Info and Desired Cash Allocation:

##### Equal Weight Rebalance - No Authorized App Enabled - Alpaca Account Info Included
   
   ```python
    #run_rebalance.py

     # .1 (10%) represents cash reserve weight 
    portfolio_rebalance = EqualWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, None, .1, config.ALPACA_BASE_URL, config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
    portfolio_rebalance.login_robinhood()
    portfolio_rebalance.rebalance()
   ```

   ```python
   #terminal

   # after cd into rebalance folder
   >>> python run_rebalance.py
   ```
    
##### Market Weight Rebalance <a name="market-weight-rebalance"></a>

The MarketWeight method takes (2) optional arugments:

* First - Minimum Drift Amount: By default this amount is set to the mandatory minimum of $1.50 - this is because Robinhood will not allow you to execute a non-position closing trade that is below $1 in total value and the additional .50 cents provides a margin of safety to ensure your trade executes even with volatile market price swings. 

However, you may set this Minimum Drift Amount $ higher than a $1.50. For example: setting the Minimum Drift Amount $ to $10 would mean that any rebalancing buy or sell transaction that falls below $10 in value would not be executed, essentially you are allowing the rebalance to drift within a $10 +/- collar range.

* Second - Minimum Equity Amount: By default this amount is set to $5, however, can be set as low as the mandatory minimum of $2.50. It may also be raised as high as you would like. 

However, the higher you raise the Minimum Equity Amount, the more likely it is that some of your current Robinhood positions do not make the cut and are dropped from your portfolio (as the funds that would be allocated to these holdings are allocated elsewhere).

In run_rebalance.py input your Robinhood and/or Alpaca Info and Desired Cash Allocation:

##### Market Weight Rebalance - No Authorized App Enabled - Alpaca Account Info Not Included
   
   ```python
    #run_rebalance.py
    
    # .1 (10%) represents cash reserve weight 
    portfolio_rebalance = MarketWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, None, .1)
    portfolio_rebalance.login_robinhood()
    portfolio_rebalance.rebalance(2.5, 10) #2.5 represents the minimum trans amount and 10 represents the min equity you desire to hold of any share 
   ```
    
   ```python
   #terminal

   # after cd into rebalance folder
   >>> python run_rebalance.py
   ```

##### Discretionary Weight Rebalance <a name="discretionary-weight-rebalance"></a>

The rebalance method on Discretionary Weight accepts only a Dictionary i.e., { SYMBOL: Fractional Weight %, SYMBOL: Fractional Weight %, ... } as an argument. 

* Note: the Stock Fractional Weight %'s + the Cash Fractional Weight % (inputted during instantiation - default is .1) must add up to 1 (100%). See Example Below For Further Clarity. 

* One More Note: the Discretionary Rebalance will close all positions that you hold in Robinhood that are not included in the Dictionary. 

Example: the values in the kwarg below add up to .9, however, when you add in the .1 inputted during instantiation you end up with 1 (100%). The rebalance will not run if this is not the case. 

##### Discretionary Weight Rebalance - No Authorized App Enabled - Alpaca Account Info Not Included
   
   ```python
    #run_rebalance.py
    
    # .1 (10%) represents cash reserve weight 
    portfolio_rebalance = DiscretionaryWeight(config.ROBIN_EMAIL, config.ROBIN_PASS, None, .1)
    portfolio_rebalance.login_robinhood()
    #2.5 represents the minimum trans amount and 10 represents the min equity you desire to hold of any share
    portfolio_rebalance.rebalance({'TSLA': .20, 'BRKB': .10, 'FB': .10, 'AAPL': .10, 'AMZN': .10,'NFLX': .10, 'GOOG': .10, 'GOOGL': .10}, 2.5, 10)
   ```
   
   ```python
   #terminal

   # after cd into rebalance folder
   >>> python run_rebalance.py
   ```

## Future Updates <a name="future-updates"></a>

* Update so users may rebalance their portfolio even if their portfolio contains stocks currently ineligible for fractionals.
* Provide rebalance features for alpaca.markets portfolios.

## License <a name="license"></a>
 
 This project is licensed under the MIT License - see the LICENSE.md file for details...
 
## Credits <a name="credits"></a>
 
 This package utilizes code from some other lovely open source packages:
 
 * [robin_stocks](https://github.com/jmfernandes/robin_stocks)
 * [alpaca-trade-api-python](https://github.com/alpacahq/alpaca-trade-api-python)
 
## Disclaimer <a name="disclaimer"></a>

The Robinhood API is 'public-ish' and may be altered at anytime by Robinhood potentially altering the performance of this package. Additionally, Robinhood may switch the manner in which it processes its order flow at anytime, which would also alter the performance of this package. Therefore, use this package at your own risk.

Additionally, contents of this repository do not constitute advice and should not be relied upon in making or refraining from making, any decision, investment or otherwise. The information herein is not intended to be investment advice. Seek a duly licensed professional for investment advice and before you make any investment decisions.

In sum, none of this investment advice, do not rely on any information, please seek investment advice from a professional financial advisor. 


 
