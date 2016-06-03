'''
Created on 3 Jun 2016
v1 : DQN agent used to trade fx
@author: purewin7
'''

import utility.stream_decode as sd

class agent():

    def __init__(self,model):
        '''
        Constructor
        '''
        self.model = model
        self.ret_series = None
        print ("new agent created!!")
    
    def feed(self,data):
        # check the time if is the point to trade
        
        # if yes, decide the action
        
        
        # implement action to the market
        
        # 
        print "agent got new ask price : " + str(sd.ask(data)) + " at " + str(sd.time(data))
        
    def decision(self):
        