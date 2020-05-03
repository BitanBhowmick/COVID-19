# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:37:51 2020

@author: Bitan
"""

import requests
import pandas as pd
import numpy as np
import re
import json


def change_dtype(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
        
def get_Tracking_Data():
    
    response = requests.get("https://api.covid19india.org/raw_data.json")
    data = response.json()

    ageList = []
    currentStatusList = []
    stateList = []
    districtList = []
    cityList = []
    genderList = []
    nationalityList = []
    dateList = []
    notesList = []
    
    try:
        for i in range (0, len(data['raw_data'])):
            ageList.append(list(data['raw_data'])[i]['agebracket'])
            currentStatusList.append(list(data['raw_data'])[i]['currentstatus'])
            stateList.append(list(data['raw_data'])[i]['detectedstate'])
            districtList.append(list(data['raw_data'])[i]['detecteddistrict'])
            cityList.append(list(data['raw_data'])[i]['detectedcity'])
            genderList.append(list(data['raw_data'])[i]['gender'])
            nationalityList.append(list(data['raw_data'])[i]['nationality'])
            notesList.append(list(data['raw_data'])[i]['notes'])
            dateList.append(list(data['raw_data'])[i]['dateannounced'])
    except:
        print('Error in Addition to List')
        
    try:
        for i in range (0,len(districtList)):
            x = districtList[i]
            if x == "Italians*":
                districtList[i] = "N/A"
    except:
        print("Italians Error")
                
    
    
    try:
        covid19DataDF = pd.DataFrame(list(zip(ageList,currentStatusList,stateList,districtList,cityList,genderList,nationalityList,notesList,dateList)),
                                        columns=['Age','Current_Status','State','District','City','Gender','Nationality','History','Effective-Date'])
        covid19DataDF = covid19DataDF.apply(lambda x: x.str.strip()).replace('', 'N/A')
        
    except:
        print('NAN Error')
        
    covidDataList = covid19DataDF.values.tolist()
    
    #covid19DataJSON = covid19DataDF.to_json(orient='records')
    j = json.dumps(covidDataList)

    return j