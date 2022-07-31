import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime

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
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Define start and end date route


@app.route("/api/v1.0/min_max_avg_temp")
def min_max_avg_temp():
    """Return the temperature value as json"""

    return jsonify()


@app.route("/api/v1.0/<start>")
def min_max_avg_temp(start_date):
    """Fetch the start date to calculate min, max and average of temperature
        for all dates greater than or equal to the start date."""

    #Convert the date value and match with dateframe? -- Day 3 Activity 09
    start = date.replace(" ", "").lower() # replace lower 
    for date in measurement:
        search_term = measurement["date"].replace("-", "").

        if search_term == start:
            return jsonify(?)

    return jsonify({"error": f"Date {real_name} is not found."}), 404

    return jsonify({f"From the date {start}, </br> the lowest temperature is {min};</br> the highest temperature is {max};</br> the average temperature is {mean}."})

@app.route("/api/v1.0/<start>/<end>")
def starts_ends():
    """Fetch the start and end date to calculate min, max and average of temperature
        for the period."""
    # Covert the date value to number? and then match with 
    start = date.replace(" ", "").lower()
    for date in measurement:
        search_term = measurement["date"].replace("-", "").

        if search_term == start:
            return jsonify(character)    
​
    # Query for data in the start and end period 
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year, ).all()
​
    # Calculate the min, max and avg temperature


    session.close()
    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


    results = measurement.query.filter(measurement.date >= datetime.strptime(start, '%Y-%m-%d'), measurement.date <= datetime.strptime(end, '%Y-%m-%d')).all()

if __name__ == "__main__":
    app.run(debug=True)
