import requests
import pandas as pd
import numpy as np
import re
import json


def get_total_daily_Updates():
    response = requests.get("https://api.covid19india.org/data.json")
    data = response.json()
    
    case_time_series_data = data['cases_time_series']
    
    data_len = len(case_time_series_data)
    #print(data_len)
    data = []
    #totalDataList = []
    
    for i in range (data_len-16, data_len):
        #print(i)
        date = case_time_series_data[i]['date']
        #print(date)
        confirmed = case_time_series_data[i]['dailyconfirmed']
        deceased = case_time_series_data[i]['dailydeceased']
        recovered = case_time_series_data[i]['dailyrecovered']
        data.append([date,confirmed,deceased,recovered])
    #totalDataList.append(data)
    
    j = json.dumps(data)
    return j
