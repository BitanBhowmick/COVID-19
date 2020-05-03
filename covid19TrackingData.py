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



def get_Data():
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
        covid19DataDF = pd.DataFrame(list(zip(ageList,currentStatusList,stateList,districtList,cityList,genderList,nationalityList,notesList,dateList)),
                                        columns=['Age','Current_Status','State','District','City','Gender','Nationality','History','Effective-Date'])
        covid19DataDF = covid19DataDF.apply(lambda x: x.str.strip()).replace('', 0)
        
    except:
        print('NAN Error')
        
    
    covid19DataJSON = covid19DataDF.to_json(orient='records')
    j = json.dumps(covid19DataJSON)

    return j


    # try:
    #     covid19DataDF.loc[:, 'Age'] = covid19DataDF['Age'].apply(change_dtype)
    # except:
    #     print('Error in converting data type')
    
    # try:
    #     for i in range (0,len(ageGroupCategorisation['Age'])):
    #         age = ageGroupCategorisation['Age'][i]
    #         if type(age) == int or type(age) == float:
    #             continue
    #         else:
    #             arr=[]
    #             print(type(age))
    #             #arr = (re.findall(r'\d+', age))
    #             arr = age.split('-')
    #             arr = [int(i) for i in arr]
    #                 #mean = int(sum(arr)) / int(len(arr))
    #                 #mean = (int(sum(arr)) / int(len(arr))) if int(len(arr) != 0 else: 0
    #             if int(len(arr)) != 0:
    #                 mean =  int(sum(arr)) / int(len(arr))
    #             else:
    #                 mean = 0
    #             ageGroupCategorisation['Age'][i] = mean
    # except:
    #     print('Error in Mean Age 1')


    # try:
    #     for i in range (0, len(ageGroupCategorisation['Age'])):
    #         age = int(ageGroupCategorisation['Age'][i])
    #         if age > 0 and age <=10:
    #             ageGroupCategorisation['Age_Category'][i] = '1-10'
    #         elif age > 10 and age <=25:
    #             ageGroupCategorisation['Age_Category'][i] = '10-25'
    #         elif age > 25 and age <=50:
    #             ageGroupCategorisation['Age_Category'][i] = '25-50'
    #         elif age > 50 and age <=70:
    #             ageGroupCategorisation['Age_Category'][i] = '50-70'
    #         elif age > 70:
    #             ageGroupCategorisation['Age_Category'][i] = 'Above 70'
    #         else:
    #             ageGroupCategorisation['Age_Category'][i] = 'Age not mentioned'
    # except:
    #     print('Error in age_categorisation')
                
                
                
                            
    # #ageGroupCategorisation.to_excel("C:\\Users\\DELL\\OneDrive\\Desktop\\ACRO\\COVID-19\\op.xlsx",sheet_name="sheet_name")

    # #ageGroupJSON = ageGroupCategorisation.to_json(orient='records')
    # d = ageGroupCategorisation.to_dict(orient='records')
    # j = json.dumps(d)

    
    # return j









    
















