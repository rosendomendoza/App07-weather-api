from flask import Flask, render_template
from search_temp import search_temp

app = Flask(__name__)

@app.route("/")
def home():
    return (render_template("home.html"))

@app.route("/api/v1/<station>/<date>")
def api(station, date):
    temperature = search_temp(station, date)
    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    app.run(debug=True)