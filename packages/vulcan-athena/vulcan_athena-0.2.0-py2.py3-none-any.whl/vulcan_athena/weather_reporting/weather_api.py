import numpy as np
import pandas as pd
import json
import datetime as dt
import time

import requests

from vulcan_athena.weather_reporting.setup import api_key, melbourne_id, geelong_id, base_url


def api_parsers(json_data):
    local_time = time.localtime(json_data["dt"])
    weather_dict = {
        "name": json_data["name"],
        "lat": json_data["coord"]["lat"],
        "lon": json_data["coord"]["lon"],
        "date": time.strftime("%Y-%m-%d", local_time),
        "time": time.strftime("%H:%M:%S", local_time),
        "weather_main": json_data["weather"][0]["main"],
        "weather_condition": json_data["weather"][0]["description"],
    }
    weather_dict.update(json_data["main"])
    weather_dict["visibility (m)"] = json_data["visibility"]
    weather_dict["clouds %"] = json_data["clouds"]["all"]
    weather_dict["wind_speed (m/s)"] = json_data["wind"]["speed"]

    return weather_dict


def df_generation(json_data):
    df = pd.DataFrame(api_parsers(json_data), index=[0])
    col_names = list(df.columns)

    col_names[7] = col_names[7] + "(C)"
    col_names[8] = col_names[8] + "(C)"
    col_names[9] = col_names[9] + "(C)"
    col_names[10] = col_names[10] + "(C)"
    col_names[11] = col_names[11] + " hPa"
    col_names[12] = col_names[12] + " %"

    df.columns = col_names

    return df
    

# main wrapper function
def main(api_key=api_key):
    # getting weather information on Melbourne
    api_address_melb = (
        base_url + "appid=" + api_key + "&id=" + melbourne_id + "&units=metric"
    )
    json_data_melb = requests.get(api_address_melb).json()

    df_melb = df_generation(json_data_melb)

    # getting weather information on Geelong
    api_address_geelong = (
        base_url + "appid=" + api_key + "&id=" + geelong_id + "&units=metric"
    )
    json_data_geelong = requests.get(api_address_geelong).json()

    df_geelong = df_generation(json_data_geelong)

    # return both the weather information together
    return df_melb.append(df_geelong)
