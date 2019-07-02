""" Xiaomi gateway sniffer """

from socket import socket, AF_INET, SOCK_DGRAM, INADDR_ANY, inet_aton, IPPROTO_IP, IP_ADD_MEMBERSHIP
import struct
import json
import re
from datetime import datetime 

# PARSE
""" Get current temperature and humidity

{
  "cmd": "report",
  "model"import re: "sensor_ht",
  "sid": "1337",
  "short_id": 54230,
  "data": "{\"temperature\":\"2351\"}"
}{
  "cmd": "report",
  "model": "sensor_ht",
  "sid": "1337",
  "short_id": 54230,
  "data": "{\"humidity\":\"5190\"}"
}
{
  "cmd": "report",
  "model": "sensor_ht",
  "sid": "1337",
  "short_id": 54230,
  "data":"{\"voltage\":3015,\"temperature\":\"2548\",\"humidity\":\"3968\"}
}

"""

def parser(payload):
    if payload['cmd'] == 'report' and payload['model'] == 'sensor_ht':
        now = datetime.now()
        timestamp = now.isoformat(timespec='seconds')
        matchTemperature = re.search(r'temperature\":\"([0-9]{4})', payload['data'])
        matchHumidity = re.search(r'humidity\":\"([0-9]{4})', payload['data'])
        if matchTemperature:
            temperatureString = matchTemperature.group(1)
            temperatureCelcius = float(temperatureString) / 100
            print(f'Current temperature at {timestamp}: {temperatureCelcius}*C')
        if matchHumidity:
            humidityString = matchHumidity.group(1)
            humidityPercent = float(humidityString) / 100
            print(f'Current humidity at {timestamp}: {humidityPercent}%')


# GET
# Todo: build function

multicast_group = '224.0.0.50'
UDPport = '9898'

sock = socket(AF_INET, SOCK_DGRAM)  # UDP Socket
sock.bind(('', 9898))
group = inet_aton(multicast_group)
mreq = struct.pack('4sL', group, INADDR_ANY)
sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

while True:
    data, who = sock.recvfrom(512)
    msg = data.decode('utf-8')
    # print(f'[{who}] {msg}')
    data = json.loads(msg)
    parser(data)

# ANALYZE: NOOP

# OUTPUT

""" Build influxDB request and send it to server """
# build JSON

"""
json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "host": "xiaomi",
            "region": "paris"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 23.51
        }
    }
        {
        "measurement": "humidity",
        "tags": {
            "host": "xiaomi",
            "region": "paris"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 51.90
        }
    }
]

"""


# Make connection
# Insert data
