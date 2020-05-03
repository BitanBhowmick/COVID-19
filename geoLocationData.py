import requests
import pandas as pd
import numpy as np
import re
import json
from datetime import datetime
from geopy.geocoders import Nominatim
import time

def change_dtype(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def get_geo_location_data():
    response = requests.get("https://api.covid19india.org/raw_data.json")
    data = response.json()
    
    geolocator = Nominatim(user_agent="test")
    #geolocator=Nominatim(timeout=10)
    
    cityList = []
    districtList = []
    
    cityValues = []
    districtValues = []
    
    for i in range (0, len(data['raw_data'])):
        city = data['raw_data'][i]["detectedcity"]
        district = data['raw_data'][i]["detecteddistrict"]
        
        if len(city) != 0:
            try:
                cityList.append(city)
                #location = geolocator.geocode(city,timeout=None)
                #cityList.append((location.latitude, location.longitude))
                #cityList = {"City": city, "Values": (location.latitude, location.longitude)}
            except:
                continue
        elif len(district) != 0:
            try:
                districtList.append(district)
                #location = geolocator.geocode(district,timeout=None)
                #districtList.append((location.latitude, location.longitude))
                #districtList = {"District": district, "Values": (location.latitude, location.longitude)}
            except:
                continue
        else:
            #print(data['raw_data'][i]["detectedstate"])
            continue
    wait = 0
    mul = 1
    
    unique_city = list(set(cityList))
    unique_district = list(set(districtList))
    
    for i in unique_city:
        location = geolocator.geocode(i, timeout=None)
        if location is not None:
            cityValues.append((location.latitude, location.longitude))
            wait = wait + 1
            if wait == (50*mul):
                time.sleep(2)
                mul = mul + 1
        
    
    for i in unique_district:
        location = geolocator.geocode(i, timeout=None)
        if location is not None:
            districtValues.append((location.latitude, location.longitude))
            wait = wait + 1
            if wait == (50*mul):
                time.sleep(2)
                mul = mul + 1
        
    listsJSON = []
    
    for i in cityValues:
        objectJSON = { "type": "Feature","properties": {},"geometry": {
            "type": "Point",
            "coordinates": i
                }
            
            }
    listsJSON.append(objectJSON)
    a = dict()
    a["features"] = []
    a["features"].append(listsJSON)
    
    return a








