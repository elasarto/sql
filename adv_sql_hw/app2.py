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
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "<b>Hawaii Climate App</b><br><br/>"
        "Available Routes:<br/>"
        "<br>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start<br/>"
        "/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    """Dates and precipitation observations from the last year"""
    # Query dates and precip values
    sel = [Measurement.date, Measurement.prcp]
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    last_year = session.query(*sel).\
    filter(Measurement.date >= year_ago).\
    order_by(Measurement.date.desc()).all()

    # Create a dictionary from the row data and append to a list of all_precip
    all_precip = []
    for year in last_year:
        precip_dict = {}
        precip_dict["date"] = year[0]
        precip_dict["prcp"] = year[1]
        all_precip.append(precip_dict)

    # Convert list of tuples into normal list
    #precip_2017 = list(np.ravel(last_year))
    
    return jsonify(all_precip)
        
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    """Return a json list of stations from the dataset"""
    # Query stations
    sel = [Station.name, Measurement.station]
    station_join = session.query(*sel).\
    filter(Measurement.station == Station.station).\
    group_by(Measurement.station).\
    order_by((Measurement.station)).all()
    
    # Convert list of tuples into normal list
    #all_stations = list(np.ravel(station_join))

    return jsonify(station_join)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    # Query all temperature observations
    #last 12 months of tobs data
    sel = [Measurement.date, Station.station, Station.name, Measurement.tobs]
        
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_join = session.query(*sel).\
        filter(Measurement.station == Station.station).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date.desc()).\
        order_by(Station.station.desc()).all()
        
    # Convert list of tuples into normal list
    #all_tobs = list(np.ravel(tobs_join))

    return jsonify(tobs_join)

@app.route("/api/v1.0/start")
def start():
    print("Server received request for 'start date' page...")
    """Return the TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""        
    sel = [Measurement.date, Measurement.tobs, func.avg(Measurement.tobs), func.max(Measurement.tobs),
           func.min(Measurement.tobs)]
    yr_date_choice = session.query(*sel).\
    filter(Measurement.date >= '2017-04-01').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
        
    # Convert list of tuples into normal list
    #date_list = list(np.ravel(yr_date_choice))
        
    return jsonify(yr_date_choice)

@app.route("/api/v1.0/start/end")
def start_end():
    print("Server received request for 'start date/end date' page...")
    """Return the TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""        
    sel = [Measurement.date, Measurement.tobs, func.avg(Measurement.tobs), func.max(Measurement.tobs),
          func.min(Measurement.tobs)]
    yr_date_choice = session.query(*sel).\
    filter(Measurement.date >= '2017-04-01', Measurement.date <= '2017-04-12').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
        
    # Convert list of tuples into normal list
    #date_list = list(np.ravel(yr_date_choice))
        
    return jsonify(yr_date_choice)

if __name__ == '__main__':
    app.run(debug=True)    