import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#dates= [{'start_date':"2017-04-01",'end_date':"2017-04-12" }]
start_date = ('2017-04-01')
end_date = ('2017-04-01')
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
        "Available Routes:<br/>"
        "<br>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start<br/>"
        "/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    """Dates and precipitation observations from the last year"""
    # Query dates and precip values
    sel = [Measurement.date, Measurement.prcp]
    year_ago = dt.date.today() - dt.timedelta(days=365)
    last_year = session.query(*sel).\
    filter(Measurement.date >= year_ago).all()

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
    """Return a json list of stations from the dataset"""
    # Query stations
    sel = [Station.name, Measurement.station]
    station_join = session.query(*sel).\
    filter(Measurement.station == Station.station).\
    group_by(Measurement.station).\
    order_by((Measurement.station)).all()
    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_join))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    # Query all temperature observations
    #last 12 months of tobs data
    sel = [Measurement.date, Station.station, Station.name, Measurement.tobs]
    #func.count(Measurement.tobs)]
        
    year_ago = dt.date.today() - dt.timedelta(days=365)
    tobs_join = session.query(*sel).\
        filter(Measurement.station == Station.station).\
        filter(Measurement.date >= year_ago).\
        order_by((Station.station)).all()
        
    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(tobs_join))

    return jsonify(all_tobs)

@app.route("/api/v1.0/start")
def start():
    """Return the TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""        
    sel = [Measurement.date, Measurement.tobs, func.avg(Measurement.tobs), func.max(Measurement.tobs),
           func.min(Measurement.tobs)]
    yr_date_choice = session.query(*sel).\
    filter(Measurement.date >= '2017-04-01').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
        
    # Convert list of tuples into normal list
    date_list = list(np.ravel(yr_date_choice))
        
    return jsonify(date_list)

@app.route("/api/v1.0/start/end")
def start_end():
    """Return the TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""        
    sel = [Measurement.date, Measurement.tobs, func.avg(Measurement.tobs), func.max(Measurement.tobs),
           func.min(Measurement.tobs)]
    yr_date_choice = session.query(*sel).\
    filter(Measurement.date >= '2017-04-01', Measurement.date <= '2017-04-12').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
        
    # Convert list of tuples into normal list
    date_list = list(np.ravel(yr_date_choice))
        
    return jsonify(date_list)

if __name__ == '__main__':
    app.run(debug=True)    