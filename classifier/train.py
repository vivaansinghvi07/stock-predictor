import pickle                                           # for storing the model
import json                                             # for reading data
import pandas as pd                                     # for creating dataframes
import numpy as np                                      # for things like mean and std dev
from sklearn.svm import SVC                             # model used to train
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
gainVariationData, volumeData, avgDailyIncreaseData, overallIncreaseData = [], [], [], []
classifications = []

# calculates the percent change of a stock
def calcPercentChange(open, close):
    return (float(close)) / float(open)

# analyses data
for stockSymbol, symbolData in data.items():        # goes through each symbol
    for number, numberData in symbolData.items():  # goes though each subset in the symbol

        # stores values
        splitIndex = int(CLASSIFYSPLIT * len(numberData.values()))
        values = list(numberData.values())[::-1]    # reversed because old days are last 
        valuesTraining = values[:splitIndex:]
        valuesTesting = values[splitIndex::]
        
        # fills array with changes
        gains = []
        volumes = []
        for dayData in valuesTraining:
            gains.append(calcPercentChange(open=dayData["1. open"], close=dayData["4. close"]))
            volumes.append(int(dayData["6. volume"]))
            
        # gets average volume
        volumeData.append(np.mean(volumes))

        # gets variation in gains
        gainVariationData.append(np.std(gains))
        avgDailyIncreaseData.append(np.mean(gains))

        # gets overall gain
        overallIncreaseData.append(calcPercentChange(open=valuesTraining[0]["1. open"], close=valuesTraining[-1]["4. close"]))

        # determines if it was worth it
        classifications.append(1 if calcPercentChange(open=valuesTesting[0]["1. open"], close=valuesTraining[-1]["4. close"]) > 1 else 0)

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
model = SVC(probability=True)
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