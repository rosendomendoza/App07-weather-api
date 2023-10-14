from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("home.html")

@app.route("/table_station/")
def table_station():
    stations = pd.read_csv("data_small/stations.txt", skiprows=17)
    stations = stations[["STAID", "STANAME                                 "]]
    return render_template("table_station.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def api(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    temperature = str(df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10)
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>/<date_from>/<date_to>")
def range(station, date_from, date_to):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    df = df.loc[df['    DATE'] >= date_from]
    df = df.loc[df['    DATE'] <= date_to]
    data_station = df.to_dict("records")
    return data_station


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    data_station = df.to_dict("records")
    return data_station


if __name__ == "__main__":
    app.run(debug=True)