# xiaomi-get-temperature
This is my first ever Python project. "Done is better than. perfect" - M. Zuckerberg
Get temperature and humidity values from Xiaomi Mi Home (LUMI) gateway and insert them into an influxDB database.

## GET
Once a temperature change is detected by the sensor, Xiaomi Mi Home gateway sends UDP datagram on multicast group 224.0.0.50 port 9898

## PARSE
JSON is parsed to extract temperature and humidity values

## ANALYZE
NOOP

## OUTPUT
Goal is to push temperature and humidity values to influxDB database to later visualize them with grafana.

## References
- InfluxDB Python to push temperature and humidity to a TSDB database: https://github.com/influxdata/influxdb-python
- Xiaomi API: https://aqara.gitbooks.io/lumi-gateway-lan-communication-api/content/message-example/temperature-and-humidity-sensor.html
- Enable Xiaomi Mi Home network functions (API): http://www.justsmarthomes.com/viewtopic.php?t=3269
- InfluxDB + grafana installation: https://towardsdatascience.com/get-system-metrics-for-5-min-with-docker-telegraf-influxdb-and-grafana-97cfd957f0ac
