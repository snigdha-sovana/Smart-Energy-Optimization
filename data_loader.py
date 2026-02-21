import pandas as pd
import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "datasets")

def load_data():
    df = pd.read_csv(os.path.join(DATA_PATH, "electricity_data.csv"))
    df = df[1110:]
    df.reset_index(drop=True, inplace=True)
    df.index = pd.to_datetime(df['Date'])

    df2 = pd.read_csv(os.path.join(DATA_PATH, "electrical_appliance_consumption.csv"))
    df2 = df2[df2['year'] == 2021]
    df2.reset_index(drop=True, inplace=True)

    df3 = pd.read_csv(os.path.join(DATA_PATH, "electrical_forecast.csv"))

    df4 = pd.read_csv(os.path.join(DATA_PATH, "electricity_appliance_wise_data.csv"))
    df4['Date'] = pd.to_datetime(df4['Date'])
    df4 = df4[df4['Date'].dt.year == 2021]
    df4.reset_index(drop=True, inplace=True)

    return df, df2, df3, df4
