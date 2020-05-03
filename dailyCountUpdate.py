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


def get_daily_count_update():

    response = requests.get("https://api.covid19india.org/data.json")
    data = response.json()

    try:
        x = data['statewise']
        for i in range (0, len(x)):
            state = x[i]['state']
            if state == 'Total':
                active = x[i]['active']
                confirmed = x[i]['confirmed']
                deaths = x[i]['deaths']
                deltaconfirmed = x[i]['deltaconfirmed'] 
                deltadeaths = x[i]['deltadeaths']
                deltarecovered = x[i]['deltarecovered']
                lastupdatedtime = x[i]['lastupdatedtime']
                recovered = x[i]['recovered']
    except:
        print('Error')
        

    try:
        y = data['tested']
        updatetimestamp = str(y[len(y)-1]['updatetimestamp'])
        totalindividualstested = str(y[len(y)-1]['totalindividualstested'])    
        totalpositivecases = str(y[len(y)-1]['totalpositivecases'])
        totalsamplestested = str(y[len(y)-1]['totalsamplestested'])
        
        updatetimestamp_prevDay = str(y[len(y)-2]['updatetimestamp'])
        totalindividualstested_prevDay = str(y[len(y)-2]['totalindividualstested'])    
        #totalpositivecases_prevDay = str(y[len(y)-2]['totalpositivecases'])
        #totalsamplestested_prevDay = str(y[len(y)-2]['totalsamplestested'])
        
        
        if totalindividualstested.isdigit() == False or totalindividualstested_prevDay.isdigit() == False:
            deltaTested = 0
        else:
            deltaTeste = abs(int(totalindividualstested) - int(totalindividualstested_prevDay))
            deltaTested = str(deltaTeste)
    except:     
        print('Error Test Case')
        
        
    
    try:
        z = data['cases_time_series']
        
        confirmed1 = z[len(z)-1]["totalconfirmed"]
        deceased1 = z[len(z)-1]["totaldeceased"]
        recovered1 = z[len(z)-1]["totaldeceased"]
        
        confirmed2 = z[len(z)-2]["totalconfirmed"]
        deceased2 = z[len(z)-2]["totaldeceased"]
        recovered2 = z[len(z)-2]["totaldeceased"]
        
        if confirmed1.isdigit() and deceased1.isdigit() and recovered1.isdigit() and confirmed2.isdigit() and deceased2.isdigit() and recovered2.isdigit():
            active1 = int(confirmed1) - int(deceased1) - int(recovered1)
            active2 = int(confirmed2) - int(deceased2) - int(recovered2)
        else:
            active1 = 0
            active2 = 0
            print("Check values for Active Delta cases in dailyCountUpdate")
        
        deltaAct = abs(active1-active2)
        deltaActive = str(deltaAct)
        
    except:
        print("Delta Active Error Parsing!!!")
    
    try:
        death_rate = round((int(deaths)/int(confirmed))*100,3)
        recovery_rate = round((int(recovered)/int(confirmed))*100,3)
    except:
        print("Death Rate and recovery rate conversion error")

    if len(totalindividualstested) == 0:
        xc_tested = totalindividualstested_prevDay
    else:
        xc_tested = totalindividualstested
        

    if len(xc_tested) == 0:
        for i in range (0, len(y)):
            tested1 = y[i]['totalindividualstested']
            if (len(tested1)) != 0:
                xc_tested = tested1
    
    
    outputJSON = { 
    "active": active,
    "confirmed":confirmed,
    "deaths":str(deaths),
    "deltaconfirmed":deltaconfirmed,
    "deltadeaths":deltadeaths,
    "deltarecovered":deltarecovered,
    "lastupdatedtime":lastupdatedtime,
    "recovered":recovered,
    "death_rate":str(death_rate),
    "recovery_rate":str(recovery_rate),
    "totalindividualstested":xc_tested,
    "totalpositivecases":totalpositivecases,
    "totalsamplestested":totalsamplestested,
    "deltaTested":str(deltaTested),
    "deltaActive":str(deltaActive)
    }
        
    jsonObj = json.dumps(outputJSON,indent=4) 

    return outputJSON




   
    
    
    
    
    
    