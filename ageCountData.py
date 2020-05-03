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
    
    
    try:
        for i in range (0, len(data['raw_data'])):
            ageList.append(list(data['raw_data'])[i]['agebracket'])
            currentStatusList.append(list(data['raw_data'])[i]['currentstatus'])
            stateList.append(list(data['raw_data'])[i]['detectedstate'])
            districtList.append(list(data['raw_data'])[i]['detecteddistrict'])
            cityList.append(list(data['raw_data'])[i]['detectedcity'])
            genderList.append(list(data['raw_data'])[i]['gender'])
            nationalityList.append(list(data['raw_data'])[i]['nationality'])
            dateList.append(list(data['raw_data'])[i]['dateannounced'])
    except:
        print('Error in Addition to List')
    
    
    #try:
    #    for i in range (0, len(data['raw_data'])):
    #        currentStatusList.append(list(data['raw_data'])[i]['currentstatus'])
    #except:
    #    print('Error in current status List')
    #
    #
    #try:
    #    for i in range (0, len(data['raw_data'])):
    #        stateList.append(list(data['raw_data'])[i]['detectedstate'])
    #except:
    #    print('Error in current state List')
    #
    #
    #try:
    #    for i in range (0, len(data['raw_data'])):
    #        districtList.append(list(data['raw_data'])[i]['detecteddistrict'])
    #except:
    #    print('Error in current detecteddistrict List')
    #
    #
    #try:
    #    for i in range (0, len(data['raw_data'])):
    #        cityList.append(list(data['raw_data'])[i]['detectedcity'])
    #except:
    #    print('Error in current cityList')
    #
    #
    #
    
    
    
    try:
        ageGroupCategorisation = pd.DataFrame(list(zip(ageList,currentStatusList,stateList,districtList,cityList,genderList,nationalityList,dateList)),
                                        columns=['Age','Current_Status','State','District','City','Gender','Nationality','Effective-Date'])
        ageGroupCategorisation = ageGroupCategorisation.apply(lambda x: x.str.strip()).replace('', 0)
    
    except:
        print('NAN Error')
    
    ageGroupCategorisation = ageGroupCategorisation.assign(Age_Category="")
    
    
    try:
        ageGroupCategorisation.loc[:, 'Age'] = ageGroupCategorisation['Age'].apply(change_dtype)
    except:
        print('Error in converting data type')
    
    try:
        for i in range (0,len(ageGroupCategorisation['Age'])):
            age = ageGroupCategorisation['Age'][i]
            if type(age) == int or type(age) == float:
                continue
            else:
                arr=[]
                #arr = (re.findall(r'\d+', age))
                arr = age.split('-')
                arr = [int(i) for i in arr]
                    #mean = int(sum(arr)) / int(len(arr))
                    #mean = (int(sum(arr)) / int(len(arr))) if int(len(arr) != 0 else: 0
                if int(len(arr)) != 0:
                    mean =  int(sum(arr)) / int(len(arr))
                else:
                    mean = 0
                ageGroupCategorisation['Age'][i] = mean
    except:
        print('Error in Mean Age 2')
    
    
    for i in range (0, len(ageGroupCategorisation['Age'])):
        age = (ageGroupCategorisation['Age']).iloc[i]
        if type(age) != int:
            print(type(age), age)
            print("Hullah")
        elif age > 0 and age <=10:
            ageGroupCategorisation['Age_Category'][i] = '1-10'
        elif age > 10 and age <=25:
            ageGroupCategorisation['Age_Category'][i] = '10-25'
        elif age > 25 and age <=50:
            ageGroupCategorisation['Age_Category'][i] = '25-50'
        elif age > 50 and age <=70:
            ageGroupCategorisation['Age_Category'][i] = '50-70'
        elif age > 70:
            ageGroupCategorisation['Age_Category'][i] = 'Above 70'
        else:
            ageGroupCategorisation['Age_Category'][i] = 'Age not mentioned'

    
    
    
    
    #ageGroupCategorisation.to_excel("C:\\Users\\DELL\\OneDrive\\Desktop\\ACRO\\COVID-19\\op.xlsx",sheet_name="sheet_name")
    
    #ageGroupJSON = ageGroupCategorisation.to_json(orient='records')
    d = ageGroupCategorisation.to_dict(orient='records')
    j = json.dumps(d)
    
    
    groups = ageGroupCategorisation.groupby('Age_Category')["Current_Status"].count()
    
    
    Category1 = str(groups['1-10'])
    Category2 = str(groups['10-25'])
    Category3 = str(groups['25-50'])
    Category4 = str(groups['50-70'])
    Category5 = str(groups['Above 70'])
    Category6 = str(groups['Age not mentioned'])
    
    
    
    outputJSON = {
        "Category1": Category1,
        "Category2": Category2,
        "Category3": Category3,
        "Category4": Category4,
        "Category5": Category5,
        "Category6": Category6
        }
    xc = outputJSON
    
    
    
    
    return xc



























