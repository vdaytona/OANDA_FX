'''
Created on 6 Jun 2016
dowonload historica data from server

@author: Daytona
'''

import oandapy
import datetime as dt
import pandas as pd

def download_his_data(pair, granularity, token):
    oanda = oandapy.API(environment="practice", access_token=token)
    all_record = get_all_record(pair, granularity, oanda)
    pd_data = put_into_pd(all_record)
    save_to_csv(pd_data, "../../Data/" + pair + ".csv")

def get_all_record(pair,granularity,oanda):
    record = []
    start_time = dt.date(2005,1,1) #yyyy-mm-dd from 2005-01-01 has 4 hour record
    end_time = dt.date(2006,1,1)
    year_dif =  dt.datetime.now().year - start_time.year + 1
    
    for i in range(year_dif) :
        if i > 0: 
            start_time = dt.date(start_time.year + 1,1,1)
            end_time = dt.date(end_time.year + 1,1,1)
        response = oanda.get_history(instrument=pair, granularity = granularity, dailyAlignment=1, \
                                      start= start_time.strftime("%Y-%m-%d"), end = end_time.strftime("%Y-%m-%d"))
        for content in response.get("candles") :
            record.append(content)
    return record
    
def put_into_pd(all_record):
    result = pd.DataFrame.from_dict(all_record)
    return result

def save_to_csv(pd_data, file_Name):
    pd_data.to_csv(file_Name)

