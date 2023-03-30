import pickle                                           # for storing the model
import json                                             # for reading data
import pandas as pd                                     # for creating dataframes
import numpy as np                                      # for things like mean and std dev
from sklearn.ensemble import RandomForestClassifier     # model used to train
from sklearn.model_selection import train_test_split    # to split data
from sklearn.preprocessing import StandardScaler        # to scale data
from sklearn.metrics import accuracy_score              # calculate accuracy
from settings import *                                  # gets all the settings

# loads data
with open(f"{DATAPATH}data.json", "r") as f:
    print("Getting data...")
    data = json.load(f)

print("Processing data...")

# defines overall arrays for data
gainVariationData, avgDailyIncreaseData, overallIncreaseData, nDayIncreaseData = [], [], [], []
classifications = []

# calculates the percent change of a stock
def calcChange(open, close):
    return (float(close)) / float(open)

# analyses data
for stockSymbol, symbolData in data.items():        # goes through each symbol
    for number, numberData in symbolData.items():  # goes though each subset in the symbol

        # stores values
        splitIndex = int((1 - CLASSIFYSPLIT) * len(numberData.values()))
        values = list(numberData.values())
        valuesTraining = values[:splitIndex:]
        valuesClassifying = values[splitIndex::]
        
        # fills array with changes
        gains = []
        for dayData in valuesTraining:
            gains.append(calcChange(open=dayData["1. open"], close=dayData["4. close"]))

        # gets variation in gains
        gainVariationData.append(np.std(gains))
        avgDailyIncreaseData.append(np.mean(gains))

        # populate nDayIncreaseData
        nDayIncreaseData.append(calcChange(open=valuesTraining[-NDAYS]["4. close"], close=valuesTraining[-1]["4. close"]))

        # gets overall gain
        overallIncreaseData.append(calcChange(open=valuesTraining[0]["4. close"], close=valuesTraining[-1]["4. close"]))

        # determines if it was worth it
        classifications.append(1 if float(valuesClassifying[0]["4. close"]) < float(valuesClassifying[-1]["4. close"]) else 0)

print("Training model...")

# puts into dataframe
frame = {}
for feature in FEATURES:
    frame[feature] = eval(feature+"Data")       # gets the array for the feature

# turns it into a pd dataframe
frame = pd.DataFrame(frame)

# splits data
trainX, testX, trainY, testY = train_test_split(frame, classifications, test_size=0.2, random_state=RANDOMSEED)    # random state for replicability

# scales model
scaler = StandardScaler()
trainX = scaler.fit_transform(trainX)
testX = scaler.transform(testX)

# creates model
model = RandomForestClassifier(random_state=RANDOMSEED**2+1)    # i tried to change my random state to get the most accuracy
model.fit(trainX, trainY)

# tests accuracy
predictedY = model.predict(testX)
print(f"The accuracy of the model is {round(accuracy_score(testY, predictedY), 4)}")

# saves models
with open(f"{MODELPATH}model.pkl", "wb") as f:
    pickle.dump(model, f)
with open(f"{MODELPATH}scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Models saved.")