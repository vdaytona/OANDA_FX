'''
Created on 2 Jun 2016
get login info for oanda

@author: purewin7
'''

class getInfo():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def get_account_id(self):
        return "7011512"
    
    def get_token(self):
        f = open("../../../token.txt","r")
        return f.readline()[:].strip()