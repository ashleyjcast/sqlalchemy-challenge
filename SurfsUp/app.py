# Import the dependencies.
import numpy as np
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
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    date_prcp = session.query(measurement.date,measurement.prcp).filter(measurement.date >= previous_year).all()
    prcp_data = {date:prcp for date, prcp in date_prcp}
    return jsonify(prcp_data)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    


# Tobs route
@app.route("/api/v1.0/tobs")
def tobs():

# Temp Routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end=None):

if __name__ == '__main__':
    app.run(debug=True)