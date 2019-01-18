# Importing necessary libraries

import pandas as pd
import os

# Importing python file that has scrape() function defined
from directory import scrape_news

from flask import (
	Flask,
	render_template,
	jsonify,
	request,
	redirect
	)

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',"sqlite:///db/warheads.sqlite")

db = SQLAlchemy(app)

class Warhead(db.Model):
	__tablename__ = 'warheads_inventories'

	Id = db.Column(db.Integer, primary_key=True)
	Country = db.Column(db.String)
	Country_code = db.Column(db.String)
	Year = db.Column(db.Integer)
	Warheads_count = db.Column(db.Integer)

	def __repr__(self):
		return '<Warhead %r>' % (self.Country)


@app.before_first_request
def setup():
	db.create_all()

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/global")
def global_data():
	results = db.session.query(Warhead.Country,Warhead.Year,func.sum(Warhead.Warheads_count).label('warhead_count')).group_by(Warhead.Year).all()
	trace9 = {}
	for result in results:
		trace9["x"] = [int(result[1]) for result in results]
		trace9["y"] = [int(result[2]) for result in results]
		trace9["name"] = "Global"
		trace9["marker"] = {"color":"#116466"}
		trace9["type"] = "bar"
	return jsonify(trace9) 

@app.route("/china")
def china_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "China").group_by(Warhead.Country, Warhead.Year).all()
	trace1 = {}
	for result in results:
		trace1["x"] = [int(result[0]) for result in results]
		trace1["y"] = [int(result[1]) for result in results]
		trace1["name"] = "China"
		trace1["marker"] = {"color":"#116466"}
		trace1["type"] = "bar"
	return jsonify(trace1)

@app.route("/france")
def france_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "France").group_by(Warhead.Country, Warhead.Year).all()
	trace2 = {}
	for result in results:
		trace2["x"] = [int(result[0]) for result in results]
		trace2["y"] = [int(result[1]) for result in results]
		trace2["name"] = "France"
		trace2["marker"] = {"color":"#116466"}
		trace2["type"] = "bar"
	return jsonify(trace2)

@app.route("/israel")
def israel_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "Israel").group_by(Warhead.Country, Warhead.Year).all()
	trace3 = {}
	for result in results:
		trace3["x"] = [int(result[0]) for result in results]
		trace3["y"] = [int(result[1]) for result in results]
		trace3["name"] = "Israel"
		trace3["marker"] =  {"color":"#116466"}
		trace3["type"] = "bar"
	return jsonify(trace3)

@app.route("/pakistan")
def pakistan_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "Pakistan").group_by(Warhead.Country, Warhead.Year).all()
	
	trace4 = {}
	for result in results:
		trace4["x"] = [int(result[0]) for result in results]
		trace4["y"] = [int(result[1]) for result in results]
		trace4["name"] = "Pakistan"
		trace4["marker"] = {"color":"#116466"}
		trace4["type"] = "bar"
	return jsonify(trace4)

@app.route("/india")
def india_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "India").group_by(Warhead.Country, Warhead.Year).all()
	trace5 = {}
	for result in results:
		trace5["x"] = [int(result[0]) for result in results]
		trace5["y"] = [int(result[1]) for result in results]
		trace5["name"] = "India"
		trace5["marker"] = {"color":"#116466"}
		trace5["type"] = "bar"
	return jsonify(trace5)

@app.route("/russia")
def russia_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "Russia").group_by(Warhead.Country, Warhead.Year).all()
	trace6 = {}
	for result in results:
		trace6["x"] = [int(result[0]) for result in results]
		trace6["y"] = [int(result[1]) for result in results]
		trace6["name"] = "Russia"
		trace6["marker"] = {"color":"#116466"}
		trace6["type"] = "bar"
	return jsonify(trace6)

@app.route("/uk")
def uk_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "United Kingdom").group_by(Warhead.Country, Warhead.Year).all()
	trace7 = {}
	for result in results:
		trace7["x"] = [int(result[0]) for result in results]
		trace7["y"] = [int(result[1]) for result in results]
		trace7["name"] = "United Kingdom"
		trace7["marker"] = {"color":"#116466"}
		trace7["type"] = "bar"
	return jsonify(trace7)

@app.route("/us")
def us_data():
	results = db.session.query(Warhead.Year, func.sum(Warhead.Warheads_count)).filter(Warhead.Country == "United States").group_by(Warhead.Country, Warhead.Year).all()
	trace8 = {}
	for result in results:
		trace8["x"] = [int(result[0]) for result in results]
		trace8["y"] = [int(result[1]) for result in results]
		trace8["name"] = "United States"
		trace8["marker"] = {"color":"#116466"}
		trace8["type"] = "bar"
	return jsonify(trace8)

#####################################################
# Creating flask-Mongodb connection
# Create Database Connection
# ----------------------------------

import pymongo
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db2 = client.nuclear_weapons
collection = db2.scraped_data

@app.route("/scrape")

def scrape():
    
    scraped_data = collection
    news_data = scrape_news.scrape()
    scraped_data.update(
        {},
        news_data,
        upsert=True
    )
    return redirect("http://localhost:5000/news", code=302)

@app.route("/news")

def query():
    # Return a single document from the scraped_data collection saved in mission_to_mars db and store it in mars_data variable
    news_data = collection.find_one()
    # pass the mars_data into an HTML template to display the data
    return render_template("news.html", news_data = news_data)

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/slider")
def slider():
    return render_template("map.html")
################
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
	app.run(debug=True)
