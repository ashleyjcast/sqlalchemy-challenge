# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
measurement = Base.classes.measurement
station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Homepage route
@app.route("/")
def welcome():
    return(
        f"Welcome to the Climate APP!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent = dt.datetime.strptime(most_recent, '%Y-%m-%d')
    previous_year = most_recent - dt.timedelta(days=365)
    date_prcp = session.query(measurement.date,measurement.prcp).filter(measurement.date >= previous_year).all()
    prcp_data = {date:prcp for date, prcp in date_prcp}
    return jsonify(prcp_data)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(station).all()
    station_list = [station.name for station in all_stations]
    return jsonify(station_list)


# Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_stations = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    stations_id = [station[0] for station in most_active_stations]
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent = dt.datetime.strptime(most_recent, '%Y-%m-%d')
    previous_year = most_recent - dt.timedelta(days=365)
    recent_year_observations = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station.in_(stations_id)).\
        filter(measurement.date >= previous_year).all()
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in recent_year_observations]
    return jsonify(tobs_data)


# Temp Routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end=None):
    if not end:
        station_temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                        filter(measurement.station >= start).all()
    else:
        station_temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                        filter(measurement.station >= start).\
                        filter(measurement.date <= end).all()
    if station_temps:
        temp_results = {
            "TMIN": station_temps[0][0], 
            "TAVG": station_temps[0][1], 
            "TMAX": station_temps[0][2]
        }
    else:
        temp_results = {
            "TMIN": None, 
            "TAVG": None, 
            "TMAX": None
            }
    return jsonify(temp_results)

if __name__ == '__main__':
    app.run(debug=True)