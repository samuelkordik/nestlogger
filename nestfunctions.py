import nest
import time
import json
import urllib2
import sched
import sys
import csv

from config import *

def logCSV(device, structure):
	# Saves ALL data locally to a CSV
	if device.mode == 'heat-cool':
		targetTemperatureLow = device.target.low
		targetTemperatureHigh = device.target.high
	else:
		targetTemperatureLow = device.target
		targetTemperatureHigh = device.target

	csv_data =[structure.away, structure.name, device.name, device.online, device.where, device.description, device.fan, device.fan_timer,device.humidity,device.mode,device.has_leaf,device.is_using_emergency_heat,device.label,device.postal_code,device.temperature_scale,device.is_locked,device.locked_temperature.low,device.locked_temperature.high,device.temperature,device.min_temperature,device.max_temperature,targetTemperatureLow,targetTemperatureHigh,device.eco_temperature.low,device.eco_temperature.high,device.hvac_state,device.previous_mode]

	nfile = open('nest_log.csv', "ab")
	writer = csv.writer(nfile)
	writer.writerow(csv_data)
	nfile.close()