from flask import Flask, render_template
from search_temp import search_temp
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    stations = pd.read_csv("data_small/stations.txt", skiprows=17)
    stations = stations[["STAID", "STANAME                                 "]]
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def api(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    temperature = str(df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10)
    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    app.run(debug=True)