""" Xiaomi gateway sniffer """

from socket import socket, AF_INET, SOCK_DGRAM, INADDR_ANY, inet_aton, IPPROTO_IP, IP_ADD_MEMBERSHIP
import struct
import json
import re
from datetime import datetime
from influxdb import InfluxDBClient

# build JSON with following sensor format to then feed influxDB


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
]
"""

def buildJSON(measure, timestamp, value, host, region):
    payload = []
    payload.append({
        "measurement": measure,
        "tags": {
            "host": host,
            "region": region
        },
        "time": timestamp,
            "fields": {
                "value": value
            }
    })

    return payload


# OUTPUT: write values and JSON into influxDB

def writeDB(jsonData):
    server = 'server.domain.org'
    port = '8086'
    username = 'admin'
    password = 'password'
    database = 'home-monitoring'
    client = InfluxDBClient(server, port, username, password, database)
    client.write_points(jsonData)
    client.close()

# PARSE
""" Get current temperature and humidity from RAW data

{
  "cmd": "report",
  "model"import re: "sensor_ht",
  "sid": "001337",
  "short_id": 54230,
  "data": "{\"temperature\":\"2351\"}"
}{
  "cmd": "report",
  "model": "sensor_ht",
  "sid": "001337",
  "short_id": 54230,
  "data": "{\"humidity\":\"5190\"}"
}
{
  "cmd": "report",
  "model": "sensor_ht",
  "sid": "001337",
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
            json_body = buildJSON('temperature', timestamp, temperatureCelcius, 'xiaomi', 'paris')
            print(json_body)
            writeDB(json_body)
        if matchHumidity:
            humidityString = matchHumidity.group(1)
            humidityPercent = float(humidityString) / 100
            print(f'Current humidity at {timestamp}: {humidityPercent}%')
            json_body  = buildJSON('humidity', timestamp, humidityPercent, 'xiaomi', 'paris')
            print(json_body)
            writeDB(json_body)

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
    print(f'[{who}] {msg}')
    data = json.loads(msg)
    parser(data)

# ANALYZE: NOOP
