# let's import all our dependencies
import numpy as np
import datetime as dt
import pandas as pd


# and let's import all the SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#finally we need to import flask dependecy
from flask import Flask, redirect, jsonify

# we now need to set up our database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# and let's reflect the database in to our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# let's also declare variables for each classes for ease of use 
Measurement = Base.classes.measurement
Station = Base.classes.station              
# we can also create the session
session = Session(engine)

#below is how we set us the flask
app = Flask(__name__)

# now we are going to create our routes, and we will put WELCOME as out=r first route
@app.route("/")
def welcome():
    return(
        "Welcome to the Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/temp/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip=precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)

