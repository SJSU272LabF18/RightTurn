import pandas as pd
import json
from flask import Flask, render_template, request

app = Flask(__name__)
county_df = pd.read_csv('data/counties.csv', engine='python',sep = ',')
posts= ''
county = 1
counties = []
collisions_df = pd.read_csv('data/collisions.csv', engine='python',sep = ',')
county_df = pd.read_csv('data/counties.csv', engine='python',sep = ',')
#screen 1 get accidents count
jsonfile=open("static/js/statesData.json")
accidents_data=json.load(jsonfile)
accidents_df = collisions_df[['CASE_ID','COUNTY']].groupby('COUNTY').count().reset_index()
for feature in accidents_data['features']:
    idx = feature['properties']['name'].upper()
    if len(accidents_df[accidents_df.COUNTY == idx]) > 0:
        feature['properties']['density'] =accidents_df[accidents_df.COUNTY == idx].CASE_ID.item()
    else:
        feature['properties']['density'] = 0
		
for i in range(len(county_df)):
	counties.append((county_df.iloc[i,0],county_df.iloc[i,1]))
@app.route("/")
@app.route("/home")

def home():
    return render_template('screen1.html',accidents_data = accidents_data)
	
@app.route("/searchbycounty")
@app.route("/searchbycounty/dataview")
def countydata():
    county = request.args.get('county',default = 1,type = int)
    return render_template('countycontents.html',counties = counties, sel_county = county)

@app.route("/searchbycounty/mapview")
def countymap():
    return render_template('countycontents.html',counties = counties, sel_county = county)

@app.route("/predictaccidents")
def predict():
    return render_template('PredictAccidents.html')
	
@app.route("/login")	
def login():
    return render_template('login.html')
	
	

if __name__ == '__main__':
	app.run(debug=True)