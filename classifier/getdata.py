import requests                         # for getting data
from datetime import date, timedelta    # for setting dates
import random                           # for random generation
import json                             # for json format
import time                             # for rate limits
from settings import *                  # import all settings

random.seed(RANDOMSEED)

# generate a random date 
def randomDay(startyear, endyear):
    
    # chooses random year and month
    year = random.randint(startyear, endyear)
    month = random.randint(1, 12)
    day = random.randint(1, 28)     # accounts for months like Feb with only 28 days

    # returns date
    return date(year, month, day)


# class for invalid API Key exception
class APIKeyException(Exception): 
    def __init__(self, message):
        self.message = message  # custom error message for many types of errors (api key not found, api key invalid, rate limited, etc)

# detects if API Key was None
if not APIKEY:
    raise APIKeyException("The environment variable \"API_KEY\" contains no key")

# defines data
data = {}

for symbol in TOPSYMBOLS:   # gets 2 per symbol

    # reset count and set the symbol to a new dictionary
    countPerSymbol = 0
    data[symbol] = {}

    # sets parameters for JSON request
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "apikey": APIKEY,
        "symbol": symbol,
        "datatype": "json",
        "outputsize": "full"
    }

    # go until proper data gotten
    while True:
        try:

            # gets json
            fullJsonData = requests.get(url, params=params).json()

            # get the entire data
            fullStockData = fullJsonData["Time Series (Daily)"]

            # break if successful
            print(f"Success for {symbol}.")
            break

        except:

            # wait for rate limit
            print(f"Rate limited at stock {symbol}. Sleeping for 1 minute.")
            time.sleep(60)
            continue

        
    # get as many as the constant states
    while countPerSymbol < DATAPERSYMBOL:

        # determines date
        day = randomDay(startyear=STARTYEAR, endyear=ENDYEAR)

        # initializes dict for sliced data
        slicedData = {}

        # gets 20 trading days before the date
        count = 0
        try:
            while count < DATACOUNT:
                # checks if day is available
                try:
                    slicedData[str(day)] = fullStockData[str(day)]
                    day += timedelta(days = 1)
                    count += 1
                except:
                    day += timedelta(days = 1)
        except OverflowError:   # detects overflow error for undetectable dates
            continue

        # adds to main data
        data[symbol][countPerSymbol] = slicedData

        # increment count
        countPerSymbol += 1

# adds to data file
with open(f"{DATAPATH}data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=True)