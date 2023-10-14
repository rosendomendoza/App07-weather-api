import pandas as pd

def search_temp (station, date):

    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return (str(temperature))
