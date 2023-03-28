import requests                         # for getting data
import os                               # for getting env variables
from datetime import date, timedelta    # for setting dates
import random                           # for random generation
import json                             # for json format
import io                               # for writing to file
import time                             # for rate limits

APIKEY = os.getenv("API_KEY")
TOPSYMBOLS = ["AAPL", "MSFT", "GOOGL", "GOOG", "TSLA", "NVDA", "JPM", "JNJ", "V", "WMT", "UNH", "PG", "MA", "HD", "DIS", "BAC", "PYPL", "ADBE", "VZ", "NFLX", "MRK", "CMCSA", "PEP", "KO", "TMO", "CRM", "ABBV", "PFE", "ABT", "ACN", "CSCO", "XOM", "CVX", "NKE", "BA", "IBM", "MDT", "MMM", "WFC"]
DATAPERSYMBOL = 3       # how many different data per symbols

# ranges for data collection
STARTYEAR = 2017
ENDYEAR = 2022
DATACOUNT = 30

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
    print("Error obtaining API Key")
    raise APIKeyException("The environment variable \"API_KEY\" contains no key")

# defines data
data = {}

for symbol in TOPSYMBOLS:   # gets 2 per symbol

    # reset count and set the symbol to a new dictionary
    countPerSymbol = 0
    data[symbol] = {}

    # get as many as the constant states
    while countPerSymbol < DATAPERSYMBOL:

        # sets parameters for JSON request
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "apikey": APIKEY,
            "symbol": symbol,
            "datatype": "json",
            "outputsize": "full"
        }

        # determines date
        day = randomDay(startyear=STARTYEAR, endyear=ENDYEAR)

        # gets json
        fullJsonData = requests.get(url, params=params).json()

        # gets data
        try:
            # get the entire data
            fullStockData = fullJsonData["Time Series (Daily)"]

            # increment the count
            countPerSymbol += 1
        except:

            # wait for rate limit
            print(f"Rate limited at stock {symbol}. Sleeping for 1 minute.")
            time.sleep(60)
            continue

        # initializes dict for sliced data
        slicedData = {}

        # gets 20 trading days before the date
        count = 0
        while count < DATACOUNT:
            # checks if day is available
            try:
                slicedData[str(day)] = fullStockData[str(day)]
                day -= timedelta(days = 1)
                count += 1
            except:
                day -= timedelta(days = 1)

        # adds to main data
        data[symbol][countPerSymbol] = slicedData

# adds to data file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=True)