'''
Created on 3 Jun 2016
to get historical data from OANDA server
@author: Daytona
'''

from utility.accountInfo import getInfo as gi
from utility import stream_decode as sd
import oandapy
import datetime as dt
from datetime import timedelta as td
import pandas as pd

def get_all_record(pair,granularity,oanda):
    record = []
    start_time = dt.date(2016,1,1) #yyyy-mm-dd from 2005-01-01 has 4 hour record
    end_time = dt.date(2017,1,1)
    year_dif =  dt.datetime.now().year - start_time.year + 1
    
    
    
    for i in range(year_dif) :
        if i > 0: 
            start_time = dt.date(start_time.year + 1,1,1)
            end_time = dt.date(end_time.year + 1,1,1)
        response = oanda.get_history(instrument=pair, granularity = granularity, dailyAlignment=1, \
                                      start= start_time.strftime("%Y-%m-%d"), end = end_time.strftime("%Y-%m-%d"))
        for content in response.get("candles") :
            #print content
            time_str = content.get("time")
            #print time_str
            record.append(content)
            
            
    #print record
    #print record[-1].get("time")
    return record

def put_into_pd(all_record):
    result = pd.DataFrame.from_dict(all_record)
    #print result
    return result

def save_to_csv(pd_data, file_Name):
    pd_data.to_csv(file_Name)

def download_his_data():
    pair = "GBP_USD"
    granularity = "H4"
    token = gi().get_token()
    #account_id = gi().get_account_id()
    
    oanda = oandapy.API(environment="practice", access_token=token)
    all_record = get_all_record(pair, granularity, oanda)
    pd_data = put_into_pd(all_record)
    #save_to_csv(pd_data, "../../Data/" + pair + ".csv")
    
    print "Finished write csv."

if __name__ == '__main__':
    download_his_data()