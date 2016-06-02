'''
Created on 2 Jun 2016

@author: Daytona
'''

import oandapy
from utility.accountInfo import getInfo as gi

class MyStreamer(oandapy.Streamer):
    def __init__(self, count=100, *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0

    def on_success(self, data):
        print data, "\n"
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()

    def on_error(self, data):
        self.disconnect()

def run():
    token = gi().get_token()
    account_id = gi().get_account_id()
    
    #print token
    #oanda = oandapy.API(environment="practice", access_token=token)
    #response = oanda.get_prices(instruments = "EUR_USD")
    #prices = response.get("prices")
    #asking_price = prices[0].get("ask")
    #print asking_price
    
    account = account_id
    
    stream = MyStreamer(environment="practice", access_token=token)
    stream.rates(account, instruments="GBP_USD",ignore_heartbeat=True)

if __name__ == '__main__':
    run()