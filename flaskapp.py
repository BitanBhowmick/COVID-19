from flask import Flask,request, jsonify
import trackingData
import stateWiseData
import dailyCountUpdate
import ageCountData
import stateDailyCount
#import getTravelHistoryData
from flask_cors import CORS
import logging
import covidResourcesData
import getDailyTotalUpdate
import subprocess
import shlex
import locationTracker
import findLocationKolkata

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


app = Flask(__name__)
CORS(app)

#app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

stateData = stateWiseData.get_StateData()
dailyCountData = dailyCountUpdate.get_daily_count_update()
ageCountData = ageCountData.get_Data()
dailyStateData = stateDailyCount.get_state_daily_count()
weeklyTotalData = stateDailyCount.get_weekly_count_total()
trackingData = trackingData.get_Tracking_Data()
covidResources = covidResourcesData.get_Covid_Resources()
dailyTotalUpdate = getDailyTotalUpdate.get_total_daily_Updates()
#travelHistoryData = ageCategoryData.get_Travel_Data()

#geoLocationData = geoLocationData.get_geo_location_data()

@app.route('/')
def hello_world():
  return '''<h1>COVID-19</h1>
<p>A prototype API for COVID-19 details.</p>'''

@app.route('/api/tracking_data', methods=['GET'])
def api_all_1():
  return trackingData


@app.route('/api/state_data', methods=['GET'])
def api_all_2():
  return stateData


@app.route('/api/get_daily_count', methods=['GET'])
def api_all_3():
  return dailyCountData
    

@app.route('/api/age_count_data', methods=['GET'])
def api_all_4():
  return ageCountData


@app.route('/api/daily_state_count', methods=['GET'])
def api_all_5():
  return dailyStateData

@app.route('/api/weekly_count', methods=['GET'])
def api_all_6():
  return weeklyTotalData


@app.route('/api/covid_resources', methods=['GET'])
def api_all_7():
  return covidResources


@app.route('/api/daily_total_updates', methods=['GET'])
def api_all_8():
  return dailyTotalUpdate


@app.route('/api/getLocation/<latitude>/<longitude>')
def api_all_9(latitude,longitude):
    print(latitude, longitude)
    jsonObj = findLocationKolkata.getKolkataLocation(latitude, longitude)
    return jsonObj

# @app.route('/api/restart', methods=['GET'])
# def execute():
#     def handle_sub_view(req):
#         from flask import request
#         request = req
#         command = 'sudo service apache2 restart'
#         #print("============")
#         command = (request.data).decode("utf-8")
#         print(command)
#         if request.method == 'POST':
#             print('Started executing command')
#             command = shlex.split(command)
#             process = subprocess.Popen(command, stdout = subprocess.PIPE)
#             print("Run successfully")
#             output, err = process.communicate()
#             return output
#         return "not executed"
#     threading.Thread.start_new_thread(handle_sub_view, (request))

# @app.route('/api/travel_data', methods=['GET'])
# def api_all_7():
#   return travelHistoryData



if __name__ == '__main__':
  app.run()