import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, request, url_for
import predictions as pred

app = Flask(__name__)
posts= ''
county = 1
counties = []
coordinates = []
jsonfile=open("static/js/statesData.json")
accidents_data=json.load(jsonfile)
collisions_df = pd.DataFrame()
county_df = pd.DataFrame()

@app.before_first_request
def function_to_run_only_once():
	#read data files
	collisions_df = pd.read_csv('data/collisions.csv', engine='python',sep = ',')
	county_df = pd.read_csv('data/counties.csv', engine='python',sep = ',')
	
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
		
@app.route("/")
@app.route("/home")

def home():
    return render_template('index.html',accidents_data = accidents_data)
	
@app.route("/searchbycounty")
@app.route("/searchbycounty/dataview")
def countydata():
    county = request.args.get('county',default = 1,type = int)
    return render_template('searchbycounty-dataview.html',counties = counties, sel_county = county)

@app.route("/searchbycounty/mapview")
def countymap():
    return render_template('searchbycounty-mapview.html',counties = counties, sel_county = county)

@app.route("/accidents-prediction")
def predictaccidents():
    return render_template('accidentsPrediction.html',coordinates = json.dumps(coordinates))
	
@app.route("/login")	
def login():
    return render_template('login.html')
	
@app.route('/predict', methods=['POST'])
def predict():
	w =  request.form['weather']
	rc =  request.form['roadCondition']
	rs =  request.form['roadSurface']
	l =  request.form['lighting']
	x =  request.form['pointx']
	y =  request.form['pointy']
	ped_involved = pred.predictPI(w,1,rc,rs,l,1640,float(x)*(-1),float(y))
	return json.dumps({'status':'OK','ped':ped_involved[0]});

if __name__ == '__main__':
	app.run(debug=True)