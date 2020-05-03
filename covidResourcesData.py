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


def get_Covid_Resources():
    
    response = requests.get("https://api.covid19india.org/resources/resources.json")
    data = response.json()
    
    covidData = data['resources']
    
    covidData.sort
    
    j = json.dumps(covidData)
    
    return j
