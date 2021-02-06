#!/usr/bin/env bash

set -e

export GEONAMES_USER=$SET_ME
export OPENWEATHER_TOKEN=$SET_ME


SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

sleep 3
python3 image_from_api.py main '"Parker, CO"' latest.png
sleep 3
python3 ./inky_show.py latest.png


cd -
