'''
Created on 2 Jun 2016

@author: Daytona
'''

import oandapy
import datetime as dt
from utility.accountInfo import getInfo as gi
from utility import stream_decode as sd
import json
import time
from pandas.algos import tiebreakers


class MyStreamer(oandapy.Streamer):
    def __init__(self, count=10, *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0

    def on_success(self, data):
        
        days = 5
        #expiryDate = time.strftime("%Y-%m-%dT%H:%M:%S",
        #                   time.localtime(int(time.time() + 86400*days)))
        time_data =  dt.datetime.strptime(str(sd.time(data)),"%Y-%m-%d %H:%M:%S")
        print time_data
        b = dt.timedelta(minutes = 15)
        a = time_data + b
        print a
        expirDate = a.strftime("%Y-%m-%dT%H:%M:%S")
        print expirDate
        #print data
        #print sd.time(data)
        #time_now_str = dt.datetime.strptime(str(sd.time(data)),"%Y-%m-%d %H:%M:%S")
        #print time_now_str.hour
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()

    def on_error(self, data):
        self.disconnect()

def download_his_data():
    token = gi().get_token()
    account_id = gi().get_account_id()
    utc_time = dt.datetime.utcnow()
    #print dt.datetime.now()
    #print type(utc_time.minute)
    
    

    
    #account = account_id
    
    stream = MyStreamer(environment="practice", access_token=token)
    stream.rates(account_id, instruments="GBP_USD",ignore_heartbeat=True)
    
    oanda = oandapy.API(environment="practice", access_token=token)
    #oanda.create_order(account_id = account_id, instrument = "GBP_USD", side = "buy", units = "1000", type = "market" )
    
    
    #===========================================================================
    # print oanda.get_account(account_id)
    # #order_id = oanda.get_trades(account_id).get("trades")[0].get("id")
    # #print order_id
    # #print type(order_id)
    # #print account_id
    # #oanda.close_trade(account_id, order_id)
    # #response = oanda.get_history(instrument="GBP_USD", granularity = "H4",start= "2015-12-18T21:00:00.000000Z", end = "2016-06-04")
    # response = oanda.get_positions(account_id)
    # print response.get("positions")
    # print oanda.get_account(account_id).get("openTrades") == 0
    # response = oanda.get_trades(account_id)
    # print response
    # response = oanda.get_transaction_history(account_id)
    # print response
    # for i in response.get("transactions") :
    #     print i
    #===========================================================================
        
        
    #response = oanda.get
    #print response
    
    
    ################################################### 10308177142
    # close trade
    
    #order_id = oanda.get_trades(account_id).get("trades")[0].get("id")
    #print order_id
    #print account_id
    #oanda.close_trade(account_id, order_id)
    ###################################################
    
    
    #===========================================================================
    # for content in response.get("candles") :
    #     print content
    # print len(response.get("candles"))
    # print "finished"
    #===========================================================================

if __name__ == '__main__':
    download_his_data()