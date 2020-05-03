import requests
import pandas as pd
import numpy as np
import re
import json
import logging
from math import radians, sin, cos, acos


# elat = radians(float(22.477576499999998))
# elon = radians(float(88.38988429999999))



def getDistance(elat,elon):
    
    elat = radians(float(elat))
    elon = radians(float(elon))
    
    response = requests.get("https://files.indiasmile.xyz/cache/infectedDistricts.json")
    if response.status_code == 200:
        data = response.json()
    else:
        print(response.status_code)
        
    dataList = [(k, v) for k, v in data.items()]
    
    coordsList = []
    
    for i in range (0, len(dataList)):
        coords = dataList[i][1]['coords']
        coordsList.append(coords)
        
    diffCoords = []
    
    for i in range (0, len(coordsList)):
        slat = radians(float(coordsList[i]['lat']))
        slon = radians(float(coordsList[i]['lng']))
        diff = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
        diffCoords.append(diff)

    return min(diffCoords)