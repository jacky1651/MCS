#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
import sys
import urllib
import Adafruit_DHT
import time
import json
import httplib
deviceId = "Ds7jNCWY"
deviceKey = "d0iDd0HeUnioG310"
def post_to_mcs(payload): 
	headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
	not_connected = 1 
	while (not_connected):
		try:
			httpClient = httplib.HTTPConnection("api.mediatek.com:80")
			httpClient.connect() 
			not_connected = 0 
		except (httplib.client.HTTPException, socket.error) as ex: 
			print ("Error: %s" % ex) 
			time.sleep(10)
			 # sleep 10 seconds
			print('123') 
	httpClient.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
	response = httpClient.getresponse() 
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
	data = response.read() 
	httpClient.close() 


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!!!
while True:
	humidity, temperature= Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":humidity}},
		{"dataChnId":"Temperature","values":{"value":temperature}}]} 
		post_to_mcs(payload)
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)
	time.sleep(10)
