'''
Created on 2 Jun 2016

@author: Daytona
'''

import oandapy

class MyStreamer(oandapy.Streamer):
    def __init__(self, count=100, *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0

    def on_success(self, data):
        print data, "\n"
        print "a"
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()

    def on_error(self, data):
        self.disconnect()

def run():
    f = open("../../../OandaToken.txt","r")
    token = f.readline()[:-1]
    print token
    #oanda = oandapy.API(environment="practice", access_token=token)
    #response = oanda.get_prices(instruments = "EUR_USD")
    #prices = response.get("prices")
    #asking_price = prices[0].get("ask")
    #print asking_price
    
    account = "vdaytona"
    stream = MyStreamer(environment="practice", access_token=token)
    stream.rates(account, instruments="EUR_USD")

if __name__ == '__main__':
    run()