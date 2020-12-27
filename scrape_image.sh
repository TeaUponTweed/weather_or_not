#!/usr/bin/env bash

set -e

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

sleep 3
python3 image_from_api.py main '"Parker, CO"' latest.png
sleep 3
python3 ./weather_display.py inky_show latest.png


cd -
