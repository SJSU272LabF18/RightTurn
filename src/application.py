import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, request, url_for, flash, redirect, session, abort
import predictions as pred
from datetime import datetime
from pedpredict import pedAccidents
from mcpredict import mcAccidents
from bcpredict import bcAccidents
from tcpredict import tcAccidents
import gviz_api
import os
from sklearn.utils import shuffle
from TimeSeriesPrediction import TimeSeriesPrediction
import mysql.connector
import time

application = app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
  user="root",
  passwd="mysql",
database="demodb"
)
mycursor = mydb.cursor()


'''ped_accidents = pedAccidents()
ped_accidents.load_model("models/pedAccidents")
mc_accidents = mcAccidents()
mc_accidents.load_model("models/mcAccidents")
bc_accidents = bcAccidents()
bc_accidents.load_model("models/bcAccidents")
tc_accidents = tcAccidents()
tc_accidents.load_model("models/tcAccidents")'''
timeSeriesPrediction = TimeSeriesPrediction()
ped_accidents = pedAccidents()
mc_accidents = mcAccidents()
bc_accidents = bcAccidents()
tc_accidents = tcAccidents()


posts= ''
county = 1
counties = []
coordinates = []
jsonfile=open("static/js/statesData.json")
accidents_data=json.load(jsonfile)
collisions_df = pd.DataFrame()
county_df = pd.DataFrame()
#screen2  preprocessing
fields = ['CASE_ID','COUNTY', 'COLLISION_SEVERITY','PCF_VIOL_CATEGORY','POINT_X','POINT_Y','PEDESTRIAN_ACCIDENT','BICYCLE_ACCIDENT','MOTORCYCLE_ACCIDENT','TRUCK_ACCIDENT','ACCIDENT_YEAR']
collisions_df_chart = pd.read_csv('data/collisions.csv', skipinitialspace=True, usecols=fields, engine='python',sep = ',')
collisions_df_chart = collisions_df_chart[collisions_df_chart.ACCIDENT_YEAR >=2016]

collisions_df_chart['PCF_VIOL_CATEGORY'] = collisions_df_chart.PCF_VIOL_CATEGORY.astype('str')
collisions_df_chart.COLLISION_SEVERITY.replace([1,2,3,4],["1 - Fatal","2 - Injury (Severe)","3 - Injury (Other Visible)","4 - Injury (Complaint of Pain)"], inplace=True)
collisions_df_chart.PCF_VIOL_CATEGORY.replace(["-","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"],["- - Not Stated","00 - Unknown","01 - Driving or Bicycling Under the Influence of Alcohol or Drug","02 - Impeding Traffic","03 - Unsafe Speed","04 - Following Too Closely","05 - Wrong Side of Road","06 - Improper Passing","07 - Unsafe Lane Change","08 - Improper Turning","09 - Automobile Right of Way","10 - Pedestrian Right of Way","11 - Pedestrian Violation","12 - Traffic Signals and Signs","13 - Hazardous Parking","14 - Lights","15 - Brakes","16 - Other Equipment","17 - Other Hazardous Violation","18 - Other Than Driver (or Pedestrian)","19 -","20 -","21 - Unsafe Starting or Backing","22 - Other Improper Driving","23 - Pedestrian or Other Under the Influence of Alcohol or Drug","24 - Fell Asleep"], inplace=True)
collisions_df_chart.PEDESTRIAN_ACCIDENT.fillna("N",inplace=True)
collisions_df_chart.BICYCLE_ACCIDENT.fillna("N",inplace=True)
collisions_df_chart.MOTORCYCLE_ACCIDENT.fillna("N",inplace=True)
collisions_df_chart.TRUCK_ACCIDENT.fillna("N",inplace=True)
description = [("CASE_ID","number"),("ACCIDENT_YEAR","number"),("COLLISION_SEVERITY","string"),("PCF_VIOL_CATEGORY","string"),
               ("PEDESTRIAN_ACCIDENT","string"),
               ("BICYCLE_ACCIDENT","string"),
               ("MOTORCYCLE_ACCIDENT","string"),
               ("TRUCK_ACCIDENT","string"),
               ("COUNTY","string"),
               ("POINT_X","string"),
               ("POINT_Y","string")]
collisions_data_table = gviz_api.DataTable(description)
data=collisions_df_chart.values
collisions_data_table.LoadData(data)
collisions_json=collisions_data_table.ToJSon()



currentdttm = datetime.now().strftime("%Y-%m-%dT%H:%M")
@app.before_first_request
def function_to_run_only_once():
    collisions_attr_df = pd.read_csv('data/surroundings.csv', engine='python',sep = ',')
    collisions_attr_df1 = pd.read_csv('data/collisions_attr_temp.csv', engine='python',sep = ',')
    temp_df = pd.concat([collisions_attr_df[['eat-drink', 'restaurant', 'snacks-fast-food', 'bar-pub', 'coffee-tea', 'coffee', 'tea', 'going-out', 'dance-night-club', 'cinema', 'theatre-music-culture', 'casino', 'sights-museums', 'landmark-attraction', 'museum', 'transport', 'airport', 'railway-station', 'public-transport', 'ferry-terminal', 'taxi-stand', 'accommodation', 'hotel', 'motel', 'hostel', 'camping', 'shopping', 'kiosk-convenience-store', 'wine-and-liquor', 'mall', 'department-store', 'food-drink', 'bookshop', 'pharmacy', 'electronics-shop', 'hardware-house-garden-shop', 'clothing-accessories-shop', 'sport-outdoor-shop', 'shop', 'business-services', 'atm-bank-exchange', 'police-emergency', 'ambulance-services', 'fire-department', 'police-station', 'post-office', 'tourist-information', 'petrol-station', 'ev-charging-station', 'car-rental', 'car-dealer-repair', 'travel-agency', 'communication-media', 'business-industry', 'service', 'facilities', 'hospital-health-care-facility', 'hospital', 'government-community-facility', 'education-facility', 'library', 'fair-convention-facility', 'parking-facility', 'toilet-rest-area', 'sports-facility-venue', 'facility', 'religious-place', 'leisure-outdoor', 'recreation', 'amusement-holiday-park', 'zoo', 'administrative-areas-buildings', 'administrative-region', 'city-town-village', 'outdoor-area-complex', 'building', 'street-square', 'intersection', 'postal-area', 'natural-geographical', 'body-of-water', 'mountain-hill', 'undersea-feature', 'forest-heath-vegetation', 'lots_of_places']],collisions_attr_df1[:50000][['PEDESTRIAN_ACCIDENT', 'BICYCLE_ACCIDENT', 'MOTORCYCLE_ACCIDENT', 'TRUCK_ACCIDENT', 'COUNT_PED_KILLED', 'COUNT_PED_KILLED.1', 'COUNT_BICYCLIST_KILLED', 'COUNT_MC_KILLED', 'COUNTY', 'CITY', 'NUMBER_KILLED', 'POINT_X', 'POINT_Y', 'weatherA', 'weatherB', 'weatherC', 'weatherD', 'weatherE', 'weatherF', 'weatherG', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'lightingA', 'lightingB', 'lightingC', 'lightingD', 'lightingE', 'road_cond_A', 'road_cond_B', 'road_cond_C', 'road_cond_D', 'road_cond_E', 'road_cond_F', 'road_cond_G', 'road_cond_H', 'road_surface_A', 'road_surface_B', 'road_surface_C', 'road_surface_D', 'collision_time']]],axis=1)
    temp_df = shuffle(temp_df).reset_index(drop = True)
    temp_df=temp_df[(np.isnan(temp_df.POINT_X) == False) & (np.isnan(temp_df.POINT_Y) == False)]
    df = temp_df[['eat-drink', 'restaurant', 'snacks-fast-food', 'bar-pub', 'coffee-tea', 'coffee', 'tea', 'going-out', 'dance-night-club', 'cinema', 'theatre-music-culture', 'casino', 'sights-museums', 'landmark-attraction', 'museum', 'transport', 'airport', 'railway-station', 'public-transport', 'ferry-terminal', 'taxi-stand', 'accommodation', 'hotel', 'motel', 'hostel', 'camping', 'shopping', 'kiosk-convenience-store', 'wine-and-liquor', 'mall', 'department-store', 'food-drink', 'bookshop', 'pharmacy', 'electronics-shop', 'hardware-house-garden-shop', 'clothing-accessories-shop', 'sport-outdoor-shop', 'shop', 'business-services', 'atm-bank-exchange', 'police-emergency', 'ambulance-services', 'fire-department', 'police-station', 'post-office', 'tourist-information', 'petrol-station', 'ev-charging-station', 'car-rental', 'car-dealer-repair', 'travel-agency', 'communication-media', 'business-industry', 'service', 'facilities', 'hospital-health-care-facility', 'hospital', 'government-community-facility', 'education-facility', 'library', 'fair-convention-facility', 'parking-facility', 'toilet-rest-area', 'sports-facility-venue', 'facility', 'religious-place', 'leisure-outdoor', 'recreation', 'amusement-holiday-park', 'zoo', 'administrative-areas-buildings', 'administrative-region', 'city-town-village', 'outdoor-area-complex', 'building', 'street-square', 'intersection', 'postal-area', 'natural-geographical', 'body-of-water', 'mountain-hill', 'undersea-feature', 'forest-heath-vegetation', 'lots_of_places', 'weatherA', 'weatherB', 'weatherC', 'weatherD', 'weatherE', 'weatherF', 'weatherG', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'lightingA', 'lightingB', 'lightingC', 'lightingD', 'lightingE', 'road_cond_A', 'road_cond_B', 'road_cond_C', 'road_cond_D', 'road_cond_E', 'road_cond_F', 'road_cond_G', 'road_cond_H', 'road_surface_A', 'road_surface_B', 'road_surface_C', 'road_surface_D','collision_time']]

    
    ped_accidents.trainModel(df,temp_df[['PEDESTRIAN_ACCIDENT']])
    
    mc_accidents.trainModel(df,temp_df[['MOTORCYCLE_ACCIDENT']])
    
    bc_accidents.trainModel(df,temp_df[['BICYCLE_ACCIDENT']])
    
    tc_accidents.trainModel(df,temp_df[['TRUCK_ACCIDENT']])
    #read data files
    collisions_df = pd.read_csv('data/collisions.csv', engine='python',sep = ',')
    county_df = pd.read_csv('data/counties.csv', engine='python',sep = ',')
    #screen2  preprocessing
    #get counties
    for i in range(len(county_df)):
        counties.append((county_df.iloc[i,0],county_df.iloc[i,1]))

    
        
    #screen 1 get accidents count
    
    accidents_df = collisions_df[['CASE_ID','COUNTY']].groupby('COUNTY').count().reset_index()
    for feature in accidents_data['features']:
        idx = feature['properties']['name'].upper()
        if len(accidents_df[accidents_df.COUNTY == idx]) > 0:
            feature['properties']['density'] =accidents_df[accidents_df.COUNTY == idx].CASE_ID.item()
        else:
            feature['properties']['density'] = 0
            
    #get coordinates to map for predictions
    temp_df=collisions_df[(np.isnan(collisions_df.POINT_X) == False) & (np.isnan(collisions_df.POINT_Y) == False)]
    for i in range(5):
        coor = {}
        coor['x'] = temp_df.iloc[i].POINT_X
        coor['y'] = temp_df.iloc[i].POINT_Y
        coordinates.append(coor)


nameV=""  
        
@app.route("/")
@app.route("/home")

def home():
    return render_template('index.html',accidents_data = accidents_data, name=nameV)
    
@app.route("/searchbycounty")
@app.route("/searchbycounty/dataview")
def countydata():
    county = request.args.get('county',default = 1,type = int)
    return render_template('countycontents.html',counties = counties, sel_county = county,data=collisions_json, name=nameV)

@app.route("/searchbycounty/mapview")
def countymap():
    return render_template('countycontents.html',counties = counties, sel_county = county,data=collisions_json, name=nameV)

@app.route("/accidents-prediction")
def predictaccidents():
    return render_template('accidentsPrediction.html',coordinates = json.dumps(coordinates),currentdttm=currentdttm,logged_in = ('logged_in' in session and session['logged_in']), name=nameV)

@app.route("/logout")
def logout():
    time.sleep(0.5)
    session['logged_in'] = False
    return redirect('/')

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        print(request.form["name"]+request.form["email"])
        sql = "INSERT INTO Users (Name, Email, Password) VALUES (%s, %s, %s)"
        values=(request.form["name"], request.form["email"], request.form["password"])
        mycursor.execute(sql,values)
        mydb.commit()

        return redirect('/')
    return render_template('Signup.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global nameV
    if request.method == 'POST':
        if request.form["password"]!='GoogleAuth' and request.form["password"]!='FacebookAuth':
            print(request.form["Name"]+request.form["email"])
            sql= "SELECT Password FROM Users where Email= %s"
            email=(request.form["email"],)
            mycursor.execute(sql,email)
            myresult=mycursor.fetchone()

            if myresult:
                if request.form['password'] != myresult[0]:
                    error = 'Invalid Credentials. Please try again.'
                else:
                    session['logged_in'] = True
                    msql= "SELECT Name FROM Users where Email= %s"
                    fetch=(request.form["email"],)
                    mycursor.execute(msql,fetch)
                    name=mycursor.fetchone()

                    nameV=name[0]
                    return redirect('/')

            else:
                error = 'Username not Present'
        else:

            nameV=request.form["name"]
            print(nameV)
            session['logged_in'] = True
            time.sleep(0.5)  
            return redirect('/')
    return render_template('RegisterFG.jshtml', error=error)
    
@app.route('/predict', methods=['POST'])
def predict():
    col_datetime =  request.form['collision_datetime']
    dt = datetime.strptime(col_datetime, "%Y-%m-%dT%H:%M")
    w =  request.form['weather']
    rc =  request.form['roadCondition']
    rs =  request.form['roadSurface']
    l =  request.form['lighting']
    x =  request.form['pointx']
    y =  request.form['pointy']
    test_df= pred.processInput(w,dt.isoweekday(),rc,rs,l,dt.time().hour*100 + dt.time().minute,float(x),float(y))
    ped_involved=ped_accidents.predict(test_df)
    mc_involved=mc_accidents.predict(test_df)
    bc_involved=bc_accidents.predict(test_df)
    tc_involved = tc_accidents.predict(test_df)
    return json.dumps({'status':'OK','pedestrians':ped_involved,'motorcyclists':mc_involved,'bicyclists':bc_involved,'trucks':tc_involved});
    
@app.route("/timeSeriesPrediction")
def forecasting():
    return render_template('timeSeriesPrediction.html',counties = counties,logged_in = ('logged_in' in session and session['logged_in']), name=nameV)

@app.route('/forecast/injured', methods=['POST'])
def forecast_injured():
    try:
        location_county =  request.form['county']
        years = int(request.form['years'])
        return timeSeriesPrediction.predict_injured(location_county, years)
    except Exception as e:
        return json.dumps({'status':'500', 'error': 'data not found'})    

@app.route('/forecast/killed', methods=['POST'])
def forecast_killed():
    try:
        location_county =  request.form['county']
        years = int(request.form['years'])
        return timeSeriesPrediction.predict_killed(location_county, years)
    except Exception as e:
        return json.dumps({'status':'500', 'error': 'data not found'})    

@app.route('/forecast/pedestrian/injured', methods=['POST'])
def forecast_pedestrian_injured():
    try:
        location_county =  request.form['county']
        years = int(request.form['years'])
        return timeSeriesPrediction.predict_pedestrian_injured(location_county, years)
    except Exception as e:
        return json.dumps({'status':'500', 'error': 'data not found'})    

@app.route('/forecast/bicyclist/injured', methods=['POST'])
def forecast_bicyclist_injured():
    try:
        location_county =  request.form['county']
        years = int(request.form['years'])
        return timeSeriesPrediction.predict_bicyclist_injured(location_county, years)
    except Exception as e:
        return json.dumps({'status':'500', 'error': 'data not found'})    

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
