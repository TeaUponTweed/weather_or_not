# Overview
A simple always-on weather display designed for use on the (inky what)[shop.pimoroni.com/products/inky-what] and the Raspberry Pi Zero W.
Makes use of (openweathermap)[https://openweathermap.org/] and (GeoNames)[https://www.geonames.org/] and you'll need a (free) API key from both of those services.
![Example Black/White Weather Image](https://github.com/Masonofagun/weather_or_not/blob/master/example_screen.png)

# Raspberry Pi Setup
## Connecting
[Given](https://www.raspberrypi.org/software/) an SD card with Raspian installed:

In `/boot/` create file called `ssh`

In `/boot/` create file called `wpa_supplicant.conf`
Populate `wpa_supplicant.conf` with:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="WIFI_SSID"
scan_ssid=1
psk="WIFI_PASSWORD"
key_mgmt=WPA-PSK
}

```
Access with:
`ssh pi@raspberrypi.local`

## System Setup

Update:
```
sudo apt-get update && sudo apt-get upgrade -y
```

Install system dependencies:
```
sudo apt-get install python-pip3
```

Optionally, add a daily reboot to keep things fresh. Run `crontab -e` as a super user and add the line
```
0 2 * * * reboot
```


# Installation
```bash
# install python dependencies from pypy
pip3 install -r requirements.txt
# install inky python libraries
curl https://get.pimoroni.com/inky | bash
```

Download fonts from google fonts, e.g. https://fonts.google.com/specimen/Nova+Mono and place them in `./fonts` and make sure the `current.ttf` symlink is pointed correctly.

Setup a cront tab to update the display every 15 minutes run `crontab -e` and add the line

```
*/15 * * * *  /path/to/repo/update_diplay.sh
```

