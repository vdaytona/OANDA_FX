'''
Created on 3 Jun 2016

@author: purewin7
'''
import sys
sys.path.append("~/git/OANDA_FX/")
from utility.accountInfo import getInfo as gi
import oandapy
from src import dqn_agent_v1
from oandapy.stream.stream import StreamerError
import utility.historical_data_download as hd

class MyStreamer(oandapy.Streamer):
    def __init__(self, agent = None, oanda = None, account_id = None, count=1000000000 , *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0
        self.agent = agent
        self.oanda = oanda
        self.account_id = account_id

    def on_success(self, data):
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()
        # monitoring is the loss is extremely
        self.agent.feed(data)

    def on_error(self, data):
        self.disconnect()

class MyStreamerError(StreamerError):
    # TODO exception
    def __init__(self,msg):
        super(MyStreamerError,self).__init__(msg)

def run():
    # get account infomation
    token = gi().get_token()
    account_id = gi().get_account_id()
    
    pair = "GBP_USD"
    look_back_term = 300
    granularity = "H4"
    
    # initial his data csv
    hd.download_his_data(pair, granularity, token)
    
    # create stream to receive realtime tick
    oanda = oandapy.API(environment="practice", access_token=token)
    
    # create a new agent
    agent = dqn_agent_v1.agent(granularity,oanda,account_id, token, pair, look_back_term)
    
    stream = MyStreamer(agent,oanda,environment="practice", access_token=token)
    try :
        stream.rates(account_id, instruments="GBP_USD",ignore_heartbeat=True)
    except MyStreamerError:
        print ("loss connection")
    
if __name__ == '__main__':
    run()