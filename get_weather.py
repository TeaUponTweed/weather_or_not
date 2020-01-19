from datetime import datetime
from datetime import timezone

from dateutil import parser

import time
import requests
import json

import cv2
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
    xticks = np.array([ix for ix in range(len(x)) if ix%2 == 0])#np.array([0,2,4,6,8,10])
    xtick_temps = [f'{t}:00' for t in time[xticks]]
    my_dpi = 50
    fig = plt.figure(figsize=(4/1.3, 3/1.3), dpi=my_dpi)
    plt.plot(x,temps, color='k', linewidth=2) # marker='s'
    plt.xticks(xticks, xtick_temps, rotation=90)
    plt.ylabel('Temp [F]')
    # plt.grid()
    plt.ylim([0,100])
    plt.tight_layout()
    fig.canvas.draw()
    fig.savefig("temp.png")

def plot_pop(pops, utc_offset):
    '''
    This code is so not DRY its embarassing
    '''
    time = np.array([int(t[0].hour + utc_offset)%24 for t in pops])
    pops = np.array([t[2]['value'] for t in pops])
    x = np.array(list(range(len(pops))))
    xticks = np.array([ix for ix in range(len(x)) if ix%2 == 0])#np.array([0,2,4,6,8,10])
    xtick_pops = [f'{t}:00' for t in time[xticks]]
    my_dpi = 50
    fig = plt.figure(figsize=(4/1.2, 3/1.2), dpi=my_dpi)
    rects = plt.bar(x,pops, color='k', linewidth=2) # marker='s'
    # for i, v in enumerate(pops):
        # ax.text(v + 3, i + .25, str(v), color='black', fontweight='bold')
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

    plt.xticks(xticks, xtick_pops, rotation=90)
    # fig.axes.get_yaxis().set_visible(False)
    plt.yticks([])


    # plt.ylabel('Chance Of Precipitation [%]')
    # plt.grid()

    plt.tight_layout()
    plt.ylim([0,100])
    plt.tight_layout()
    fig.canvas.draw()
    fig.savefig("pop.png")
    # X = np.array(fig.canvas.renderer.buffer_rgba())
    # fig, ax = plt.subplots()
    # ax.imshow(X)
    # print(X)
    # plt.show()


def choose_icon(snippet):
    snippet = snippet.lower()
    if 'snow' in snippet:
        icon = '.icons/weather_snowy'
    elif 'rain' in snippet:
        icon = '.icons/weather_rainy'
    elif 'wind' in snippet or 'breeze' in snippet:
        icon = '.icons/weather_windy'
    elif 'cloud' in snippet or 'fog' in snippet:
        icon = '.icons/weather_cloudy'
    else:
        icon = '.icons/weather_sunny'

    return icon


def get_weather():
    # get text snippets
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

    # get hourly forcast
    utc_offset = time.localtime().tm_gmtoff / 3600
    raw_data = requests.get(
        "https://forecast.weather.gov/MapClick.php?lat=39.556&lon=-104.794&unit=0&lg=english&FcstType=json"
    ).json()
    raw_data = requests.get("https://api.weather.gov/gridpoints/TOP/68,52").json()
    temps = raw_data["properties"]["temperature"]['values']
    pops = raw_data["properties"]["probabilityOfPrecipitation"]['values']
    temps = get_rolling_time_series(temps, 12)
    pops = get_rolling_time_series(pops, 12)
    plot_temp(temps, utc_offset)
    plot_pop(pops, utc_offset)
    pop_arr = cv2.imread("pop.png", cv2.IMREAD_GRAYSCALE) > 200
    # pop_arr = cv2.cvtColor(pop_arr, cv2.COLOR_BGR2GRAY)
    temp_arr = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE) > 200
    f, ax = plt.subplots()
    ax.hist(pop_arr.flatten())
    f,ax = plt.subplots()

    ax.imshow(pop_arr)
    plt.show()
    # temp_arr = cv2.cvtColor(temp_arr, cv2.COLOR_BGR2GRAY)
    print(pop_arr)
    # print type(im)
    # print(temps)
    # print(snippets)
    # print(raw_data)
    # print(utc_offset/3600)


if __name__ == "__main__":
    get_weather()
