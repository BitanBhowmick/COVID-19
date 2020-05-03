import requests
import json

def change_dtype(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def get_StateData():

    response = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
    data = response.json()

    jsonData = json.dumps(data)

    return jsonData