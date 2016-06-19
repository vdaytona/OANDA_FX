'''
Created on 3 Jun 2016
v1 : DQN agent used to trade fx
@author: purewin7
'''


import utility.stream_decode as sd
import datetime as dt
import pandas as pd
from keras.models import model_from_json
import json
import numpy as np
import utility.historical_data_download as hd



class agent():

    def __init__(self,granularity,oanda,account_id, token, pair, look_back_term):
        '''
        Constructor
        '''
        global ACTION_LIST
        
        self.account_id = account_id
        self.pair = pair
        self.granularity = granularity
        self.oanda = oanda
        self.token = token
        self.look_back_term = look_back_term
        self.ACTION_LIST = ["buy","no_trade","sell"]
        self.leverage = 2.5
        self.order_id = self.get_order_id()
        
        self.model = self.build_model()
        self.csv_data = self.read_csv_data()
        self.ret_series = self.get_ret_series()
        self.side = self.get_side()
        self.last_trading_hour = self.get_last_trading_hour()
        self.next_trading_hour = self.get_next_trading_hour()
        self.time = None
        
        
        print ("new DQN agent created!!")
    
    def get_last_trading_hour(self):
        hour_csv = sd.timeRFC(self.csv_data["time"].values[-1]).hour
        return hour_csv
    
    def get_next_trading_hour(self):
        if self.last_trading_hour + 4 >= 24 :
            next_trading_hour = self.last_trading_hour + 4 -24
        else :
            next_trading_hour = self.last_trading_hour + 4
        return next_trading_hour
    
    def update_trading_hour(self):
        self.last_trading_hour = self.get_last_trading_hour()
        self.next_trading_hour = self.get_next_trading_hour()
    
    def get_order_id(self):
        if self.oanda.get_account(self.account_id).get("openTrades") != 0 :
            return self.oanda.get_trades(self.account_id).get("trades")[0].get("id")
        else :
            return None
    
    def update_order_id(self):
        self.order_id = self.get_order_id()
    
    def read_csv_data(self):
        fileName = "../../Data/GBP_USD.csv"
        data = pd.read_csv(fileName,header=0)
        return data
    
    def get_ret_series(self):
        compelte_data = self.csv_data[self.csv_data["complete"] == True]
        close = compelte_data["closeAsk"].values
        return (close[1:] - close[:-1])
    
    def update_csv_data(self):
        self.csv_data = self.read_csv_data()
    
    def update_ret_series(self) :
        self.ret_series = self.get_ret_series()
        
    def update_his_data_csv(self):
        hd.download_his_data(self.pair, self.granularity, self.token)
        self.update_csv_data()
        self.update_ret_series()
        candle_time = self.csv_data["time"].values[-1]
        print "Update the historical data at " + candle_time + " ."
    
    def build_model(self):
        model_name = "../model/DRL_model_oanda_v7_17"
        with open(model_name+ ".json", "r") as jfile:
            model = model_from_json(json.load(jfile))
        model.load_weights(model_name + ".h5")
        model.compile("sgd", "mse")
        print "Prediction model has built."
        return model
    
    def get_side(self):
        if self.oanda.get_account(self.account_id).get("openTrades") != 0 :
            side = self.oanda.get_positions(self.account_id).get('positions')[0].get('side')
        else :
            side = "no_trade"
        return side
    
    def close_trade(self):
        order_id = self.oanda.get_trades(self.account_id).get("trades")[0].get("id")
        self.oanda.close_trade(self.account_id, order_id)
        
    def create_order(self,oanda, account_id, pair, side, unit , trade_type, price, **params):
        oanda.create_order(self.account_id, instrument = pair, side = side, unit = unit, type = trade_type ,params=params)
        
    def get_state(self):
        state_retrun =  self.ret_series[-1 * self.look_back_term:]
        state_np = np.zeros((1,self.look_back_term))
        state_np[0:1] = state_retrun
        return state_np
    
    def get_last_closebid(self):
        compelte_data = self.csv_data[self.csv_data["complete"] == True]
        last_close_bid = compelte_data["closeAsk"].values[-1]
        return last_close_bid
    
    def check_update_time(self,data):
        minute = dt.datetime.strptime(str(sd.time(data)),"%Y-%m-%d %H:%M:%S").minute
        result = minute >= 0 and minute < 2
        return result
    
    def decide_action(self, state):
        q_value = self.model.predict(state)
        print q_value
        if abs(q_value[0] - q_value[2]) >= 0.002 :
            return np.argmax(q_value)
        else :
            return 1
        
    
    def feed(self,data):
        self.time = dt.datetime.strptime(str(sd.time(data)),"%Y-%m-%d %H:%M:%S")
        
        # check the balance
        #print self.oanda.get_account(self.account_id)
        
        # check the time if is the point to update csv
        
        if self.check_update_time(data) :
            hour_server = self.time.hour
            if hour_server == self.next_trading_hour : # not consider the end of week
                # update csv
                self.update_his_data_csv()
                
                # check if csv has been successfully updated by comparing last hour to hour_server
                csv_hour = self.get_last_trading_hour()
                
                if csv_hour == hour_server :
                    # get state as model input
                    state = self.get_state()
                    
                    # action 
                    #action = np.argmax(self.model.predict(state))
                    action = self.decide_action(state)
                    
                    # trade
                    self.trade(action,data)
                    
                    # update next trading hour
                    self.update_trading_hour()
                    
                    # update order id
                    self.update_order_id()
        
        if np.random.randint(10) == 1 :
            print "Agent got new ask price : " + str(sd.ask(data)) + " at " + \
            str(sd.time(data)) + " (GMT Time), next trading hour is at " + str(self.next_trading_hour) + ":00"
        
    def trade(self,action,data):
        
        side = self.ACTION_LIST[action]
        print "Previous side : " + self.side
        print "Next side : " + side
        # if next action same, do nothing
        # close present trade if need to change trade
        if self.side is not "no_trade" and self.side != side:
            self.close_trade()
            print ("Close " + self.pair + " trade at") # TODO
        # open new trade
        if self.side != side and action != 1 :
            margin_avail = self.oanda.get_account(self.account_id).get('marginAvail')
            investment = self.leverage * margin_avail
            price = self.get_last_closebid()
            side = self.ACTION_LIST[action]
            expirDate = self.time+ dt.timedelta(minutes = 30)
            expirDate = expirDate.strftime("%Y-%m-%dT%H:%M:%S")
            #self.oanda.create_order(account_id = self.account_id, instrument = "GBP_USD", \
            #                        units = int (investment / price), side = side, type = "limit", price = price, expiry = expirDate)
            self.oanda.create_order(account_id = self.account_id, instrument = "GBP_USD", \
                                    units = int (investment / price), side = side, type = "market")
            print ("Place market order " + side + " at " + str(price)) # TODO
        self.side = side