import pandas as pd
from flask import Flask, render_template, request
app = Flask(__name__)
county_df = pd.read_csv('data/counties.csv', engine='python',sep = ',')
posts= ''
county = 1
counties = []
for i in range(len(county_df)):
	counties.append((county_df.iloc[i,0],county_df.iloc[i,1]))
@app.route("/")
@app.route("/home")

def hello():
    return render_template('screen1.html',posts = posts)
	
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