import nest
import time
import json
import urllib2
import sched
import sys

from config import *

napi = nest.Nest(client_id=client_id, client_secret=client_secret, access_token_cache_file=access_token_cache_file)

print('Checking authorization...')

if napi.authorization_required:
    print('Go to ' + napi.authorize_url + ' to authorize, then enter PIN below')
    if sys.version_info[0] < 3:
        pin = raw_input("PIN: ")
    else:
        pin = input("PIN: ")
    napi.request_token(pin)

for structure in napi.structures:
    for device in structure.thermostats:
        print 'Mode       : %s' % device.mode
        print 'Temp       : %0.1f' % device.temperature
        print 'Target     : %0.1f' % device.target
structure = napi.structures[0]

# Maybe later have current temp, maybe using pyowm
#if structure.away:
#    data = {'value1': device.temperature, 'value2': awaytemp, 'value3': structure.weather.current.temperature}
#else:
#    data = {'value1': device.temperature, 'value2': device.target, 'value3': structure.weather.current.temperature}



awayValue = 'Home/'
if structure.away:
	awayValue = 'Away/'

data = {'value1': awayValue + '/' + device.mode + '/' + device.hvac_state + '/fan '+str(device.fan),'value2': str(device.temperature) + ' (' + str(device.target) + ')','value3': str(device.humidity)}
req = urllib2.Request('https://maker.ifttt.com/trigger/logtemperature/with/key/kbbmhSZNpxGDaf4wo-ZXn3qGr9kZdNZUqKkl-RqRwWW') # Replace XXX with your IFTTT Maker Key
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))