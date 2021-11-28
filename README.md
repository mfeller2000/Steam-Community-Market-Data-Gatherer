# Steam Community Market Data Collector
This Script collects the Bid/Ask Prices of an Item on the Steam Community Market and stores it in a MySQL/MariaDB Database
# Requirements
Install via PIP the following packages:

    pip3 install requests mysql-connector-python

Then edit the File and enter your Database Credentials (Host, User, Password and Database)

# Starting
This Script requires 5 Arguments:

 1. Is the Interval that the Script will pull Data from Steam (e.g. every 60 Seconds)
 2. The Item ID, you will have to find out the ID, by looking for example in the Network in your Browser that you want to pull the Data from. (e.g. This ID 176264317 correspond to this Item  https://steamcommunity.com/market/listings/730/Operation%20Riptide%20Case)
 3. Is the Currency ID in what Format the Prices will be shown (1 = $, 2 = £, 3 = €, ...)
 4. Is the Country code, but it shouldn't matter what you choose
 5. Is the Language, like the Country Code, it shouldn't matter

Example:

    python3 steam_market_collector.py 60 176264317 1 DE german
