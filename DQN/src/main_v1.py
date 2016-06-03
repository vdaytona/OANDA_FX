'''
Created on 3 Jun 2016

@author: purewin7
'''

from utility.accountInfo import getInfo as gi
import oandapy
import agent_v1

class MyStreamer(oandapy.Streamer):
    def __init__(self, agent = None, count=100 , *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0
        self.agent = agent

    def on_success(self, data):
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()
        self.agent.feed(data)

    def on_error(self, data):
        self.disconnect()

def start():
    # get account infomation
    token = gi().get_token()
    account_id = gi().get_account_id()
    
    # create a new agent
    agent = agent_v1.agent()
    
    # create stream to receive realtime tick
    stream = MyStreamer(agent,environment="practice", access_token=token)
    stream.rates(account_id, instruments="GBP_USD",ignore_heartbeat=True)
    
    oanda = oandapy.API(environment="practice", access_token=token)
    response = oanda.get_prices(instruments="EUR_USD")

if __name__ == '__main__':
    start()