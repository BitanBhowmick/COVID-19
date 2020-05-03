import requests
import pandas as pd
import numpy as np
import re
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def get_state_daily_count():
    
    try:
        response1 = requests.get("https://api.covid19india.org/data.json")
        if response1.status_code == 200:
            data1 = response1.json()
        else:
            response1.status_code
    except Exception as e:
        logging.error("Exception occurred in get_state_daily_count", exc_info=True)
        print('stateDailyCount:',response1.status_code)
        

    x1 = data1['statewise']
    length_x = len(x1)

    stateDataList = {}

    try:
        for i in range (0, length_x):
            keys = x1[i]['state']
            values = x1[i]
            stateDataList[keys] = values
    except Exception as e:
        logging.error("Exception occurred in get_state_daily_count", exc_info=True)
        print('Daily State Eror')


    listStateData = [(k, v) for k, v in stateDataList.items()]
    
    dictStates = {
        "Ladakh":"1137",
        "Jammu and Kashmir":"10039",
        "Himachal Pradesh":"4226",
        "Punjab":"10611",
        "Uttarakhand":"4473",
        "Haryana":"17582",
        "Delhi":"30560",
        "Uttar Pradesh":"45483",
        "Rajasthan":"74484",
        "Gujarat":"42384",
        "Madhya Pradesh":"35076",
        "Bihar":"14924",
        "Sikkim":"80",
        "Arunachal Pradesh":"496",
        "Assam":"5514",
        "Nagaland":"543",
        "Manipur":"0",
        "Mizoram":"135",
        "Tripura":"3215",
        "Meghalaya":"1046",
        "West Bengal":"7990",
        "Jharkhand":"5380",
        "Odisha":"23433",
        "Chhattisgarh":"9220",
        "Maharashtra":"95210",
        "Telangana":"16827",
        "Andhra Pradesh":"54338",
        "Karnataka":"35958",
        "Goa":"1116",
        "Kerala":"21940",
        "Tamil Nadu":"72403",
        "Andaman and Nicobar Islands":"2304",
        "Daman and Diu": "0",
        "Chandigarh":"638",
        "Dadra and Nagar Haveli":"0",
        "Lakshadweep":"0",
        "Puducherry":"1184"
    }

    stateList = [(k, v) for k, v in dictStates.items()]
    
    for i in range (0, len(listStateData)):
        for j in range (0, len(stateList)):
            state = stateList[j][0]
            if state == listStateData[i][0]:
                listStateData[i][1]["Tested"] = stateList[j][1]
                
    
    testList = listStateData
    
    for i in range (0, len(testList)-1):
        value = testList[i][0]
        if value == "Total":
            totalDetails = testList[i]
            del testList[i]
            
    testList.sort()
    testList.append(totalDetails) 
        
    j = json.dumps(testList)
    
    logging.error("Exception occurred in get_state_daily_count", exc_info=True)
    
    return j

def get_weekly_count_total():
    response = requests.get("https://api.covid19india.org/data.json")
    data = response.json()
    
    case_time_series_data = data['cases_time_series']
    
    weekly_dates = []
    confirmed = []
    deceased = []
    recovered = []
    
    for i in range (0, len(case_time_series_data), 7):
        #index1 = case_time_series_data[i]
        if i == 0:
             continue
        else:
             index1 = case_time_series_data[i]
             weekly_dates.append(case_time_series_data[i]["date"])
             confirmed.append(case_time_series_data[i]["totalconfirmed"])
             deceased.append(case_time_series_data[i]["totaldeceased"])
             recovered.append(case_time_series_data[i]["totalrecovered"])
             
    
    try:
        weeklyCountData = pd.DataFrame(list(zip(weekly_dates,confirmed,deceased,recovered)),
                                          columns=['Date','Confirmed','Death','Recovered'])
        
    except:
        print('NAN Error')
    
    logging.error("Exception occurred in get_weekly_count_total", exc_info=True)
    
    der = weeklyCountData.to_dict(orient='records')
    jer = json.dumps(der)
    
    logging.error("Exception occurred", exc_info=True)
    
    return jer
    

