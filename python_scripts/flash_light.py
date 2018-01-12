
delay = 2
flashes = 5

entity_id = data.get('entity_id')
hass.services.call('light', 'turn_on', { 'entity_id': entity_id })
time.sleep(delay/2)

now_state = hass.states.get(entity_id)

logger.info('current %s' % now_state)

state = now_state.state
logger.info('state %s' % state)

my_data = {}
for k,v in data.items():
    logger.info('adding %s,%s' % (k,v))
    my_data[k] = v

current = {}
for k,v in now_state.attributes.items():
    logger.info('adding to current %s,%s' % (k,v))
    current[k] = v


logger.info('my_data %s' % my_data)

if 'delay' in my_data:
    delay = my_data.get('delay')
    del my_data['delay']

if 'flashes' in my_data:
    flashes = my_data.get('flashes')
    del my_data['flashes']


cache = { 'entity_id': entity_id }
logger.info('initial cache %s' % cache)

if 'brightness' in current:
    cache['brightness'] = current.get('brightness')

if 'color_temp' in current:
    cache['color_temp'] = current.get('color_temp')

if 'rgb_color' in current:
    cache['rgb_color'] = current.get('rgb_color')

elif 'xy_color' in current:
    cache['xy_color'] = current.get('xy_color')


logger.info('final cache %s' % cache)
for i in range(0, flashes):
    logger.info('flash')
    time.sleep(delay/2)
    hass.services.call('light', 'turn_on', my_data )
    time.sleep(delay/2)
    hass.services.call('light', 'turn_off', { 'entity_id': entity_id })

logger.info('restore')
hass.services.call('light', 'turn_on', cache )

if state == 'off':
    hass.services.call('light', 'turn_off', { 'entity_id': entity_id })

