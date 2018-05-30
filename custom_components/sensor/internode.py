"""
Support for Internode Bandwidth Monitor.

"""
from datetime import timedelta
import logging
import asyncio
import async_timeout
import aiohttp

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_MONITORED_VARIABLES, CONF_NAME, CONF_USERNAME, CONF_PASSWORD)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

import xml.etree.ElementTree as ET

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'internode'

GIGABYTES = 'GB'  # type: str
BYTES = 'bytes'  # type: str
PERCENT = '%'  # type: str

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)
REQUEST_TIMEOUT = 5  # seconds

CONF_SERVICE_ID = "service"

SENSOR_TYPES = {
    'usage': ['Usage', PERCENT, 'mdi:percent'],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MONITORED_VARIABLES):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_SERVICE_ID): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the sensor platform."""

    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    serviceid = config.get(CONF_SERVICE_ID)

    auth = aiohttp.BasicAuth( username, password=password)
    websession = async_get_clientsession(hass)

    ts_data = StartInternodeData(hass.loop, websession, auth, serviceid)
    ret = yield from ts_data.async_update()
    if ret is False:
        _LOGGER.error("Invalid Internode Credentials")
        return

    name = config.get(CONF_NAME)
    sensors = []
    for variable in config[CONF_MONITORED_VARIABLES]:
        sensors.append(StartInternodeSensor(ts_data, variable, name))

    async_add_devices(sensors, True)


class StartInternodeSensor(Entity):
    """Representation of Internode Bandwidth sensor."""

    def __init__(self, startinternodedata, sensor_type, name):
        """Initialize the sensor."""
        self.client_name = name
        self.type = sensor_type
        self.startinternodedata = startinternodedata

        self._name = SENSOR_TYPES[sensor_type][0]
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._icon = SENSOR_TYPES[sensor_type][2]

        self._state = None
        self._state_attrs = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format(self.client_name, self._name)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs

    @asyncio.coroutine
    def async_update(self):
        """Get the latest data from Internode and update the state."""
        yield from self.startinternodedata.async_update()

        quota = self.startinternodedata.data.get('quota')
        used = self.startinternodedata.data.get('used')

        self._state_attrs.update({
                "quota": quota,
                "used": used,
                "traffic_unit": self.startinternodedata.data.get('unit'),
                "rollover": self.startinternodedata.data.get('rollover'),
                "plan_interval": self.startinternodedata.data.get('plan-interval')
        })

        if quota and used:
          self._state = "%.2f" % ( int(used) / int(quota) * 100)




class StartInternodeData(object):
    """Get data from Internode API."""

    def __init__(self, loop, websession, auth, service_id):
        """Initialize the data object."""
        self.loop = loop
        self.auth = auth
        self.websession = websession
        self.service_id = service_id
        self.data = { 'quota': None, 'traffic': None, 'plan-interval': None, 'rollover': None, 'unit': None }

    @staticmethod
    def bytes_to_gb(value):
        """Convert from bytes to GB.

        :param value: The value in bytes to convert to GB.
        :return: Converted GB value
        """
        return float(value) * 10 ** -9

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Get the Internode bandwidth data from the web service."""
        _LOGGER.debug("Updating Internode usage data")
        url = 'https://customer-webtools-api.internode.on.net/api/v1.5/%s/usage' % self.service_id

        with async_timeout.timeout(REQUEST_TIMEOUT, loop=self.loop):
            req = await self.websession.get(url, auth=self.auth)
        if req.status != 200:
            _LOGGER.error("Request failed with status: %u", req.status)
            return False

        data = await req.text()

        tree = ET.fromstring(data)
        error_message = tree.find('error/msg')
        assert error_message is None, "Request failed. Server responded with an error: %s" % error_message.text
        #return tree

        traffic_tree = tree.find('api/traffic')

        for i in ['name', 'plan-interval', 'rollover', 'unit']:
            self.data[i] = traffic_tree.get(i)

        self.data['quota'] = int(traffic_tree.get('quota'))
        self.data['used'] = int(traffic_tree.text)

        _LOGGER.info(self.data)

        return True
