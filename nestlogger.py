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

######
# Additional code here for WeatherUnderground local weather conditions and
# for Google Sheets data formatting from Reddit u/bucketybuckbuck.
#
# Added geolookup code and cooling/AC values.
#
######


# WeatherUnderground requires an api key. Sign up here http://www.wunderground.com/weather/api/ for a key,
# then insert that key into the config file.


# url="http://api.wunderground.com/api/"+apikey+"/conditions/q/UK/<nearestlocation>.json" example for outside of US.

if structure.country_code == "US":
	url="http://api.wunderground.com/api/"+apikey+"/conditions/q/US/"+structure.postal_code+".json"



meteo=urllib2.urlopen(url).read()
meteo = meteo.decode('utf-8')
weather = json.loads(meteo)
cur_temp =weather['current_observation']['temp_f']
cur_humid = weather['current_observation']['relative_humidity']
cur_wind_deg = weather['current_observation']['wind_degrees']
cur_wind_mph =weather['current_observation']['wind_mph']
cur_pressure = weather['current_observation']['pressure_in']
cur_dewpoint = weather['current_observation']['dewpoint_f']
cur_solar = weather['current_observation']['solarradiation']
cur_hourly_precip = weather['current_observation']['precip_1hr_in']
cur_weather = weather['current_observation']['weather']



heatValue = 0;
coolValue = 0;
if device.hvac_state == 'heating':
	heatValue = 25
elif device.hvac_state == 'cooling':
	coolValue = 25


data = {'value1': str(heatValue) + "|" + str(coolValue) +"|"+str(device.temperature)+"|"+str(device.target)+"|"+str(device.humidity)+"|"+str('cur_temp')+"|"+str('cur_humid')+"|"+str('cur_wind_deg')+"|"+str('cur_wind_mph')+"|"+str('cur_pressure')+"|"+str('cur_dewpoint')+"|"+str('cur_solar')+"|"+str('cur_hourly_precip')+"|"+str('cur_weather')
,'value2': '=(SPLIT(INDIRECT(CONCAT(\"B\", ROW())), \"|\"))'}

data = {'value1': awayValue + '/' + device.mode + '/' + device.hvac_state + '/fan '+str(device.fan),'value2': str(device.temperature) + ' (' + str(device.target) + ')','value3': str(device.humidity)}
req = urllib2.Request('https://maker.ifttt.com/trigger/logtemperature/with/key/kbbmhSZNpxGDaf4wo-ZXn3qGr9kZdNZUqKkl-RqRwWW') # Replace XXX with your IFTTT Maker Key
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))

