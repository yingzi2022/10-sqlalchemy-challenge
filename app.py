import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Define a homepage and list all available routes.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"List all Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# 1. Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date and prcp values"""
    # Query measurement table
    results = session.query(measurement.date,measurement.prcp).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of prcp values
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    # Dict with date as the key and prcp as the value
    # precip = {date: prcp for date, prcp in precipitation}

    return jsonify(all_prcp)

# 2. Define station route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of station"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station"""
    # Query measurement table
    stn = session.query(station.station).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_stn = list(np.ravel(stn))

    return jsonify(all_stn)


# 3. Define temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Define the most active station
    # active_stn = session.query(station.station).order_by(func.count(station.station).desc()).\
    #     group_by(station.station).first()
    
    # print(active_stn)
    # Need to make sure the above returned value is a string.  If it is a list, then 
    #  active_stn = session.query(station.station).order_by(func.count(station.station).desc()).\
    #     group_by(station.station).first().(0) -- as the first value of the list

    """Return the temperature data for the last year"""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    temp = session.query(measurement.tobs).\
        filter(measurement.date >= prev_year).filter(measurement.station == 'USC00519523').all()

    session.close()
    
    # Convert list of tuples into normal list
    all_temp = list(np.ravel(temp))
    
    return jsonify(all_temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None,end=None):
    """Fetch the start and end date to calculate min, max and average of temperature
        for the period."""

    session = Session(engine)

    # Covert the date value to number? and then match with 
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    
    if end :
        end = dt.datetime.strptime(end, "%Y-%m-%d")
    else :
        end = dt.datetime.today()

    # Query for data in the start and end period 
    temperature = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    # Calculate the min, max and avg temperature

    session.close()
    # Dict with date as the key and prcp as the value
    all_temp2 = list(np.ravel(temperature))
    
    return jsonify(all_temp2)

if __name__ == "__main__":
    app.run(debug=True)
