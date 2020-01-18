from datetime import datetime
from datetime import timezone

from dateutil import parser

import time
import requests
import json

import matplotlib.pyplot as plt
import numpy as np

# import pytz
from tzlocal import get_localzone # $ pip install tzlocal

# following instructions here https://www.weather.gov/documentation/services-web-api
# and example https://github.com/JulianNorton/weather-milliseconds/blob/master/app.py
def get_rolling_time_series(vals, ntake):
    now = datetime.now(timezone.utc)
    # print(now)
    # now = now.astimezone(get_localzone())
    out = []
    for val in vals:
        dt = parser.parse(val['validTime'].split('/')[0])
        # print(dt)
        dt = dt.replace(tzinfo=timezone.utc)
        # print(dt)
        # dt.tzingo
        delta = dt - now
        ts = delta.total_seconds()
        if ts > -3600:
            out.append((dt, delta, val))

        if len(out) == ntake:
            break

    assert len(out) == ntake

    return out

# def plot_data(values, ax):
    # for i in range(len(values)):
        # print()
        # print(dt)
    # print(now//3600)%24

def plot_temp(temps, utc_offset):
    time = np.array([int(t[0].hour + utc_offset)%24 for t in temps])
    temps = np.array([t[2]['value'] for t in temps])*9/5 + 32
    x = np.array(list(range(len(temps))))
    xticks = np.array([0,2,4,6,8,10])
    xtick_temps = [f'{t}:00' for t in time[xticks]]
    my_dpi = 50
    plt.figure(figsize=(4, 3), dpi=my_dpi)
    plt.plot(x,temps, color='k', marker='s', linewidth=2)
    plt.xticks(xticks, xtick_temps, rotation=0)
    plt.ylabel('Temp [F]')
    plt.grid()
    plt.tight_layout()
    # plt.show()


def get_weather():
    # get text snippets
    '''
    raw_data = requests.get(
        "https://forecast.weather.gov/MapClick.php?lat=39.556&lon=-104.794&unit=0&lg=english&FcstType=json"
    ).json()
    current = raw_data['time']['startPeriodName'][0]
    names = [
        "Today",
        "Tonight",
        "Tomorrow Morning",
        "Tomorrow Night"
    ]
    if current == 'Tonight':
        names = names[1:]
    snippets = dict(zip(names, raw_data['data']['weather']))
    '''
    # get hourly forcast
    utc_offset = time.localtime().tm_gmtoff / 3600
    raw_data = requests.get(
        "https://forecast.weather.gov/MapClick.php?lat=39.556&lon=-104.794&unit=0&lg=english&FcstType=json"
    ).json()
    raw_data = requests.get("https://api.weather.gov/gridpoints/TOP/68,52").json()
    temps = raw_data["properties"]["temperature"]['values']
    pops = raw_data["properties"]["probabilityOfPrecipitation"]['values']
    temps = get_rolling_time_series(temps, 12)
    plot_temp(temps, utc_offset)
    # print(temps)
    # print(snippets)
    # print(raw_data)
    # print(utc_offset/3600)


if __name__ == "__main__":
    get_weather()
