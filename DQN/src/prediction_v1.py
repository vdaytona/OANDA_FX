'''
Created on 6 Jun 2016

@author: Daytona
'''
import pandas as pd
from keras.models import model_from_json
import json
import numpy as np
import utility.stream_decode as ds

def download_his_data():
    input_data = "GBP_USD.csv"
    # import return data from oanda data
    data = pd.read_csv("../../Data/" + input_data,header=0)
    
    compelte_data = data[data["complete"] == True]
    print compelte_data[-2:]
    
    hour_csv = data["time"].values[-1]
    print ds.timeRFC(hour_csv).hour
    
    print hour_csv
    #print data
    close = data["closeAsk"].values
    #print close
    training_period_start = -300
    state = (close[1:] - close[:-1])[training_period_start -1: -1]
    print state[-1]
    print len(state)
    
    state_np = np.zeros((1,300))

    
    state_np[0:1] = state 
    print state_np
    model_name = "../model/DRL_model_v7_2016-06-05-07-10-15"
    with open(model_name+ ".json", "r") as jfile:
        model = model_from_json(json.load(jfile))
    model.load_weights(model_name + ".h5")
    model.compile("sgd", "mse")
    
    q = model.predict(state_np)
    print q
    print ["buy","no entry","sell"][np.argmax(q)]

if __name__ == '__main__':
    download_his_data()