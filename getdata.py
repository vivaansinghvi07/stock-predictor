import requests                         # for getting data
import os                               # for getting env variables
from datetime import date, timedelta    # for setting dates
import random                           # for random generation
import json                             # for json format
import io                               # for writing to file

APIKEY = os.getenv("API_KEY")
TOPSYMBOLS = ["AAPL", "MSFT", "GOOGL", "GOOG", "TSLA", "NVDA", "JPM", "JNJ", "V", "WMT", "UNH", "PG", "MA", "HD", "DIS", "BAC", "PYPL", "ADBE", "VZ", "NFLX", "MRK", "CMCSA", "PEP", "KO", "TMO", "CRM", "ABBV", "PFE", "ABT", "ACN", "CSCO", "XOM", "CVX", "NKE", "BA", "IBM", "MDT", "MMM", "WFC"]

# ranges for data collection
STARTYEAR = 2017
ENDYEAR = 2022

# generate a random 30-day interval
def random30Days(startyear, endyear):
    
    # chooses random year and month
    year = random.randint(startyear, endyear)
    month = random.randint(1, 12)
    day = random.randint(1, 28)     # accounts for months like Feb with only 28 days

    # gets the date
    start = date(year, month, day)

    # returns date and date of 30 days in the future
    return str(start), str(start + timedelta(days=30)) 


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

for symbol in TOPSYMBOLS:

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
    start, end = random30Days(startyear=STARTYEAR, endyear=ENDYEAR)

    # gets data
    fullStockData = requests.get(url, params=params).json()["Time Series (Daily)"]

    # slices data according to dates
    slicedData = {tradingDay: info for tradingDay, info in fullStockData.items() if start <= tradingDay <= end}

    # adds to main data
    data[symbol] = slicedData

# adds to data file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=True)