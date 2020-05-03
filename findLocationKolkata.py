from math import radians, cos, sin, asin, sqrt
import pandas as pd


def haversine(lon1, lat1, lon2, lat2):
  # convert decimal degrees to radians 
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 
  r = 6371 # Radius of earth in kilometers. Use 3956 for miles
  return c * r



def getKolkataLocation(elat, elon):

    #kolkataDataDF = pd.read_excel('C:\\Users\\DELL\\OneDrive\\Desktop\\ACRO\\COVID-19\\API\\Test_Codes_COVID-19\\Kolkata-Places.xlsx')
    kolkataDataDF = pd.read_excel('/var/www/html/covid-19/Kolkata-Places.xlsx')
    
    
    kolkataDataDF = kolkataDataDF.assign(Difference = "")  
    
    elat = float(elat)
    elon = float(elon)
    
    kolkataDataList = kolkataDataDF.values.tolist()
    
    for i in range (0, len(kolkataDataList)):
        slat = float(kolkataDataList[i][1].split(',')[0])
        slon = float(kolkataDataList[i][1].split(',')[1])
        diff = haversine(slon, slat, elon, elat)
        kolkataDataList[i][2] = diff
        
    diffList = []
    
    for i in range (0, len(kolkataDataList)):
        diffList.append(kolkataDataList[i][2])
    
    pos = int(diffList.index(min(diffList)))
    
    location = kolkataDataList[pos][0]
    coords = kolkataDataList[pos][1]
    difference = str(min(diffList))
    
    jsonObj = {
        "Location":location,
        "Latitude":coords.split(',')[0],
        "Longitude":coords.split(',')[1],
        "Difference":difference
        }
    
    return jsonObj
