import requests
import json
import pandas as pd
from geotext import GeoText
import pycountry
#import nlp
import spacy
import re

nlp = spacy.load('en_core_web_sm')

def change_dtype(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def extract_places(input):
    cities = []
    countries = []
    alpha_2 = []
    arr_places = []
    
    doc = nlp(input)
    lists = doc.ents
    
    for i in lists:
        places = GeoText(str(i))
        if len(places.country_mentions) != 0:
            alpha_2 = list(places.country_mentions.items())
            for i in range (0, len(alpha_2)):
                arr_places.append(pycountry.countries.get(alpha_2=alpha_2[i][0]).name)
        elif len(input) != 0:
            arr = (re.split(r'\s+', input))
            for i in arr:
                if i == "UK":
                    arr_places.append("United Kingdom")
        else:
            name = pycountry.countries.get(alpha_2=str(lists[0])).name
            arr_places.append(name)
            
    return arr_places
        
        
        
    # places = GeoText(input)
    # cities.append(places.cities)
    # countries.append(places.countries)
    # alpha_2 = list(places.country_mentions.items())
    # for i in range (0, len(alpha_2)):
    #     arr_places.append(pycountry.countries.get(alpha_2=alpha_2[i][0]).name)
    
    # return arr_places

def get_Travel_Data():
    response = requests.get("https://api.covid19india.org/raw_data.json")
    data = response.json()
    
    ageList = []
    travelHistoryList = []
    #countryVisitedList = []
    currentStatusList = []
    stateList = []
    districtList = []
    cityList = []
    genderList = []
    nationalityList = []
    typeOfTransmissionList = []
    dateList = []
    
    
    
    try:
        for i in range (0, len(data['raw_data'])):
            ageList.append(list(data['raw_data'])[i]['agebracket'])
            stateList.append(list(data['raw_data'])[i]['detectedstate'])
            districtList.append(list(data['raw_data'])[i]['detecteddistrict'])
            cityList.append(list(data['raw_data'])[i]['detectedcity'])
            genderList.append(list(data['raw_data'])[i]['gender'])
            nationalityList.append(list(data['raw_data'])[i]['nationality'])
            dateList.append(list(data['raw_data'])[i]['dateannounced'])
            travelHistoryList.append(list(data['raw_data'])[i]['notes'])
            typeOfTransmissionList.append(list(data['raw_data'])[i]['typeoftransmission'])
            
    except:
        print('Error in Addition to List')
    
    
    try:
        travel_DataDF = pd.DataFrame(list(zip(ageList,stateList,districtList,cityList,genderList,nationalityList,dateList,travelHistoryList,typeOfTransmissionList)),
                                          columns=['Age','State','District','City','Gender','Nationality','Effective-Date','Travel_History','Type_Of_Transmission'])
        travel_DataDF = travel_DataDF.apply(lambda x: x.str.strip()).replace('', 'N/A')
    except:
        print('NAN Error')
    
    travel_DataDF = travel_DataDF.assign(Travelled_Countries = "")
    
    list1 = []
    
    for i in range (0, len(travel_DataDF['Type_Of_Transmission'])):
        travelType = str(travel_DataDF['Type_Of_Transmission'][i])
        if travelType == 'Imported':
            travel_DataDF['Travelled_Countries'][i] = extract_places(travelHistoryList[i])
        elif travelType == 'Local':
            travel_DataDF['Travelled_Countries'][i] = 'None'
        elif travelType == '0':
            travel_DataDF['Travelled_Countries'][i] = 'N/A'
        else:
            travel_DataDF['Travelled_Countries'][i] = 'Not Disclossed'
        
    dfobj = travel_DataDF.head(100)    
    d = dfobj.to_dict(orient='records')
    j = json.dumps(d)
    
    return j

    
    
# subSet = travel_DataDF[["Current_Status","Type_Of_Transmission","Travelled_Countries"]]   
   
# listOfAllCountries = []

# for i in range (0, len(subSet["Type_Of_Transmission"])):
#     method = subSet["Type_Of_Transmission"][i]
#     if method == 'Imported':
#         travelled_countries = subSet["Travelled_Countries"][i]
#         for j in range (0, len(travelled_countries)):
#             listOfAllCountries.append(travelled_countries[j])


# uniqueCountries = list(set(listOfAllCountries))


# for name_of_countries in subSet["Travelled_Countries"]:
#     for country in name_of_countries:
#         if country in uniqueCountries:
            
            









    
#travel_DataDF.to_excel("C:\\Users\\DELL\\OneDrive\\Desktop\\ACRO\\COVID-19\\op.xlsx",sheet_name="sheet_name")

#jsonData = json.dumps(data)
