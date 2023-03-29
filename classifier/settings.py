# ALL SETTINGS GO HERE
APIKEY = ""

# these are the symbols the model is trained with 
TOPSYMBOLS = ["AAPL", "MSFT", "GOOGL", "GOOG", "TSLA", "NVDA", "JPM", "JNJ", "V", "WMT", "UNH", "PG", "MA", "HD", "DIS", "BAC", "PYPL", "ADBE", "VZ", "NFLX", "MRK", "CMCSA", "PEP", "KO", "TMO", "CRM", "ABBV", "PFE", "ABT", "ACN", "CSCO", "XOM", "CVX", "NKE", "BA", "IBM", "MDT", "MMM", "WFC"]

# how many pieces of data per symbol
DATAPERSYMBOL = 4

# ranges for data collection
STARTYEAR = 2017        # EARLIEST YEAR FOR DATA
ENDYEAR = 2022          # LATEST YEAR FOR DATA
DATACOUNT = 20          # NUMBER OF DAYS IN DATA INTERVAL

# random seed for replicability
RANDOMSEED = 10

# features for analysis (only changing these wont do anything, but they're here so you can see what is being looked at)
FEATURES = ["gainVariation", "volume", "avgDailyIncrease", "overallIncrease"]

# what percent of the data to use for classification determination
CLASSIFYSPLIT = 0.20        

# path to folder
MODELPATH = "classifier/models/"       # folder destination for model
DATAPATH = "classifier/"
IPYNBMODELPATH = "models/"