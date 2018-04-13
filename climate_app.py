import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the dates and temp obs from the last year
    # Convert the query to a dict using date as the key and tobs as the value
    # Return the json representation of your dictionary
    results = session.query(Measurements.date, Measurements.tobs).all()

    all_results = []
    for result in results:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["tobs"] = result.tobs
        all_results.append(result_dict)
    
    return jsonify(all_results)

@app.route("/api/v1.0/stations")
def stations():
    # Return a json list of stations from the dataset
    results = session.query(Stations.station).all()
    
    all_results = []
    for result in results:
        result_dict = {}
        result_dict["station"] = result.station
        all_results.append(result_dict)
    
    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    #Return a json list of tobs for the previous year
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date >= "2017-01-01").filter(Measurements.date <= "2017-12-31").all()

    all_results = []
    for result in results:
        all_results.append(result.tobs)
    
    return jsonify(all_results)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def weather_report(start=None, end=None):
    try:
        if end==None:
            [(tmin, tavg, tmax)] = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).all()

            return jsonify([(tmin, tavg, tmax)])
        
        else:
            [(tmin, tavg, tmax)] = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()

            return jsonify([(tmin, tavg, tmax)])
    except:
        return jsonify("Please input your date as YYYY-MM-DD")


if __name__ == "__main__":
    app.run(debug=True)