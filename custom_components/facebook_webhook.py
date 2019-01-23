"""
Support for Inbound Facebook Messages
"""
import asyncio
import async_timeout
import copy
import enum
import logging
import uuid

from aiohttp import web, ClientError

from datetime import datetime

import voluptuous as vol

from urllib.parse import parse_qsl
from homeassistant.core import callback
from homeassistant.const import HTTP_BAD_REQUEST
from homeassistant.helpers import intent, template, config_validation as cv
from homeassistant.components import http
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'facebook_webhook'

CONF_ALLOWED = 'allowed_ids'
CONF_VERIFY_TOKEN = 'verify_token'
CONF_ACCESS_TOKEN = 'access_token'

TIMEOUT = 5

HOOK_SCHEMA = vol.Schema({
        vol.Required(CONF_VERIFY_TOKEN): cv.string,
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Required(CONF_ALLOWED, default=[]): vol.All(cv.ensure_list, [cv.string]),
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: HOOK_SCHEMA
}, extra=vol.ALLOW_EXTRA)

WEBHOOK_ENDPOINT = '/api/facebook_webhook'


class WebhookIntentsView(http.HomeAssistantView):
    """Handle Facebook requests."""

    url = WEBHOOK_ENDPOINT
    name = 'api:facebook_webhook'
    requires_auth = False
    config = None

    def __init__(self, config):
        self.config = config

    def init(self, config):
        self.config = config

    @asyncio.coroutine
    def get(self, request):
        hass = request.app['hass']
        path = request.path
        relurl = request._rel_url

        config_verify = self.config[CONF_VERIFY_TOKEN]
        v = relurl.query

        verify = v.get('hub.verify_token')
        challenge = v.get('hub.challenge')
        mode = v.get('hub.subscribe')

        if verify == config_verify:
            return web.Response(text=challenge, status=200)

        return web.Response(text='OK', status=200)
        
    @asyncio.coroutine
    def post(self, request):
        """Handle Facebook Message ."""
        hass = request.app['hass']
        data = yield from request.json()

        config_verify = self.config[CONF_VERIFY_TOKEN]
        allowed = self.config[CONF_ALLOWED]
        token = self.config[CONF_ACCESS_TOKEN]

        entries = data.get('entry')
        for entry in entries:

            for msg in entry.get('messaging'):
                sender = msg.get('sender', {'id': None}).get('id', None)
                _LOGGER.error('INCOMING MESSAGE FROM %s' % sender)

                if sender in allowed: 
                    message = msg.get('message')
                    text = message.get('text')
                    _LOGGER.debug('Passing %s to conversation' % text)

                    hass.async_add_job(self.process_command(token, hass, sender, text))
                    return web.Response(text='OK', status=200)
                else:
                    _LOGGER.error('Sender ID %s is not in allowed list' % sender)
                    hass.async_add_job(self.send_response(token, hass, sender, 'Sorry, I have not been authorised to accept commands from you.'))
                    return web.Response(text='OK', status=200)


    @asyncio.coroutine
    def process_command(self, access_token, hass, sender, message):
        result = yield from hass.services.async_call('conversation', 'process', { 'text': message }, blocking=True)
        return result


    @asyncio.coroutine
    def send_response(self, access_token, hass, recipient, message):
        response_data = {
                "recipient": {
                    "id": recipient
                },
                "message": {
                    "text": message
                }
        }

        try:
            websession = async_get_clientsession(hass)
            with async_timeout.timeout(TIMEOUT, loop=hass.loop):
                response = yield from websession.post('https://graph.facebook.com/v2.10/me/messages', 
                        params={'access_token': access_token}, json=response_data)
                if response.status != 200:
                    _LOGGER.error("Query failed, response code: %s Full message: %s", response.status, response)
                    return False

                data = yield from response.json()

        except (asyncio.TimeoutError, ClientError) as error:
            _LOGGER.error("Failed communicating with Facebook: %s", type(error))
            return False

        return data
            


@asyncio.coroutine
def async_setup(hass, config):
    conf = config.get(DOMAIN)
    _LOGGER.error("Setup CONFIG %s" % conf)
    if conf is None:
        conf = HOOK_SCHEMA({})

    hass.http.register_view(WebhookIntentsView(conf))
    return True
