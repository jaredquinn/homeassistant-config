
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
* Xiaomi Aqara Temperature & Humidity Sensor (x2)
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
* NodeMCU MQTT w/Submersible Temperature Sensor (Aquarium)
* NodeMCU MQTT Lounge Room Humidity/Temperature/Pressure
* NodeMCU MQTT Bedroom Temperature/Humidity Sensor
* NodeMCU MQTT RFID Scan In/Out
* ESP32 based MQTT Display Panel
* Front Door Reed Sensor (wired to RFID Scanner)
* Dangerous Prototypes USB IRToy (Infrared Recevier/Sender)
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


# INTERNODE SENSOR

Internode are an Australian Internet service provider; this sensor shows the current percentage quota utilisation for the current billing period.  Additional information is supplied in the additional attributes including total bytes used, total quota, period end date and period type.  

## Installation

Copy the custom_components/sensors/internode.py file to your configuration directory including the hirearchy (create custom_component/sensors if you don't already have one).

## Configuration

Add the following block to your configuration, with your Internode username (not including any @internode.on.net) and password and your service ID which you can find by following the instructions below.

```yaml
sensor:
- platform: internode
  username: test
  password: test
  service: 123456
  monitored_variables:
    - usage
    
```

### Getting your Service ID

You can find your ServiceID by going to https://customer-webtools-api.internode.on.net/api/v1.5 and enter your Internode credentials (without any @internode.on.net) and you can find your service ID in the XML returned, where SERVICE_ID is shown:

```XML
<?xml version="1.0" encoding="UTF-8"?>
<internode>
    <api>
        <services count="1">
            <service type="Personal_ADSL" href="/api/v1.5/SERVICE_ID">SERVICE_ID</service>
        </services>
    </api>
</internode>
```


