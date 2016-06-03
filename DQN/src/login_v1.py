'''
Created on 2 Jun 2016

@author: Daytona
'''

import oandapy
import datetime
from utility.accountInfo import getInfo as gi
from utility import stream_decode as sd
import json

class MyStreamer(oandapy.Streamer):
    def __init__(self, count=100, *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0

    def on_success(self, data):
        print data
        print sd.time(data)
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()

    def on_error(self, data):
        self.disconnect()

def run():
    token = gi().get_token()
    account_id = gi().get_account_id()
    
    account = account_id
    
    stream = MyStreamer(environment="practice", access_token=token)
    stream.rates(account, instruments="GBP_USD",ignore_heartbeat=True)
    
    print "finished"

if __name__ == '__main__':
    run()