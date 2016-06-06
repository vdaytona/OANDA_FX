'''
Created on 3 Jun 2016
decode the stream
e.g.
{"tick": {"ask": 1.44607,"instrument": "GBP_USD","bid": 1.44586,"time": "2016-06-02T14:06:15.500418Z"}}
return the ask price, instrument , bid , time
@author: Daytona
'''
from datetime import datetime as dt

def ask(stream_input):
    return float(stream_input["tick"]["ask"])

def instrument(stream_input):
    return stream_input["tick"]["instrument"]

def bid(stream_input):
    return float(stream_input["tick"]["bid"])

def time(stream_input):
    time_str = stream_input["tick"]["time"]
    time_str = dt.strptime(time_str[:time_str.index(".")], '%Y-%m-%dT%H:%M:%S')
    return time_str

def timeRFC(time_rfc):
    time_str = dt.strptime(time_rfc[:time_rfc.index(".")], '%Y-%m-%dT%H:%M:%S')
    return time_str