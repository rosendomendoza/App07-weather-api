from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

DATA_PATH = "data_small"

# Show Homepage
@app.route("/")
def home():

    return render_template("home.html")


# Show Table Station
@app.route("/table_station/")
def table_station():
    stations = pd.read_csv(DATA_PATH+"/stations.txt", skiprows=17)
    stations = stations[["STAID", "STANAME                                 "]]
    return render_template("table_station.html", data=stations.to_html())


# For a given station, Return the data for a particular day
@app.route("/api/v1/day/<station>/<date>")
def api(station, date):
    filename = DATA_PATH+"/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    temperature = str(df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10)
    return {"station": station,
            "date": date,
            "temperature": temperature}


# For a given station, Return the data for a date range
@app.route("/api/v1/range/<station>/<date_from>/<date_to>")
def range(station, date_from, date_to):
    filename = DATA_PATH+"/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    df = df.loc[df['    DATE'] >= date_from]
    df = df.loc[df['    DATE'] <= date_to]
    data_station = df.to_dict("records")
    return data_station


# For a given station, Return the data for a particular year
@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = DATA_PATH+"/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))]
    data_station = result.to_dict("records")
    return data_station


# Return all data of a particular station
@app.route("/api/v1/all/<station>")
def all_data(station):
    filename = DATA_PATH+"/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    data_station = df.to_dict("records")
    return data_station


if __name__ == "__main__":
    app.run(debug=True)