
# Home Assitant Configuration

Welcome to my Home Assistant Configuration.   If you haven't come across Home Assistant before, you really should check it out first.
You can find it at https://www.home-assistant.io/.

My Home Assistant Configuration is a work in progress and is subject to change on a whim.  It's here for your inspiration or for use
as an example. 

## Software Ecosystem

* Ubuntu 18.04 running on an Intel NUC
* Mosquitto MQTT Broker
* MariaDB (mysql) Database
* VLC

* Token Authentication (MQTT RFID Validator)

* Facebook Messenger Notifications

## Smart Home Devices

* Google Home
* Amazon Echo Dot (via Home Assistant Cloud)
* Xiaomi Aqara Gateway Night Light
* Xiaomi Aqara Smart Button (x3)
* Xiaomi Aqara Temperature & Humidity Sensor
* Xiaomi Aqara Door/Window Switch
* Xiaomi Aqara Motion Detection (x2)
* YeeLight Color LED Light Bulb (x4)
* TP-Link Color LED Light Bulb
* TP-Link White LED Light Bulb
* Broadlink RM2 Pro WiFi Infra-Red Blaster
* Broadlink SP3Mini WiFi A/C Switch (x2)
* Google Chromecast
* Roku
* TP-Link HS100 WiFi A/C Switch
* NodeMCU w/Submersible Temperature Sensor
* NodeMCU Outdoor Temperator Sensor (coming soon)
* NodeMCU RFID Scanner
* Dangerous Prototypes USB IRToy (Infrared Recevier/Sender)
* ESP32 based MQTT Display Panel
* Bluetooth Remote Control (for Lights)
* Sonic Screwdriver (coming soon)

## TTS and Extras

* PicoTTS
* Google TTS
* VLC Media Player

## Device Tracking

* GPSLogger
* Network Ping
* MQTT Device Tracker (RFID Scanner)

## Weather

* BOM Australia
* Forecast (NDK)
* Weatherunderground
* Sun


## Additional Features

* MQTT HA Alarm Panel
* Floorplan
* lirc IR Remote (using IRToy)
* Bluetooth Keyboard Remote
* InfluxDB
* Facebook Messanger

## Custom Components

* Internode Usage API (Australian ISP)  - custom_components/sensors/internode.py
* Facebook Webhooks

## Modified Core Components

* myvlc - VLC Media Player with bugfixes
* new_georss_feed - geo_rss_feed with publish event features

## Python Scripts

* Remote Control (channel to IR mapping, key sequence support)

# FLOOR PLAN

pkozul's ha-floorplan is configured, as per his instructions at https://github.com/pkozul/ha-floorplan.

I generated my floorplan.svg using InkScape on Linux.

* Trace the basic wall layout of the house from an existing format.
* Paste SVG objects from other floorplans, such as couches
* Find relevant icons on Material Design Icons
* Assign HA IDs to the relevant SVG Objects

You will find a default floorplan at floorplan.svg.dist,  please contact me privately if you require 
a copy of my floorplan SVG.

# SECRETS

The secrets.yaml.dist file is generated on updates of my secrets file and does
not contain any values, only the keys.  This can be used as a starting point
for using HA Secrets.

Additionally some files are included from a 'secret' directory; these will
ultimately be migrated to the secrets.yaml file.

# ZONES

Configuration includes some sample zones for nearby places that are frequented,
if you wish to override your 'home' and 'work' zones, create files in the 
'zones' directory.

Additional "secret" zones are not included in this repository and are prefixed
as secret_* in the filename.

