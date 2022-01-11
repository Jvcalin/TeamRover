
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxdbMeasurement:
	def __init__(self, rover, sensor):
		self.rover = rover  #rover name (roger) is the influxdb database
		self.sensor = sensor
		self.measurement = "sensor"  # the measurement will always be sensor, this is so we can store other kinds
		self.url = "http://192.168.86.39:8086"
		self.token = ""
		client = influxdb_client.InfluxDBClient(url=self.url, token=self.token)
		self.write_api = client.write_api(write_options=SYNCHRONOUS)
		self.tags = {"sensor": sensor}

	def post(self, fields):
		point = influxdb_client.Point(self.measurement)
		for t in self.tags.keys():
			point.tag(t, self.tags[t])
		for f in fields.keys():
			point.field(f, fields[f])
		self.write_api.write(bucket=self.rover, org="", record=point)

# def test():
# 	database = "teamrover"
# 	token = ""
# 	# Store the URL of your InfluxDB instance
# 	url = "http://192.168.86.39:8086"
#
# 	client = influxdb_client.InfluxDBClient(url=url, token=token)
# 	write_api = client.write_api(write_options=SYNCHRONOUS)
#
# 	p = influxdb_client.Point("roger")  #
# 	p.tag("sensor", "accelerometer")
# 	p.field("x", 25.3)
# 	p.field("y", 23.9)
# 	p.field("z", 88)
#
# 	write_api.write(bucket=database, org="", record=p)
# # client = influxdb_client.InfluxDBClient(
# # 	url=url,
# # 	token=token,
# # 	org=org
# # )
# #
# # write_api = client.write_api(write_options=SYNCHRONOUS)
# #
# # p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
# # write_api.write(bucket=bucket, org=org, record=p)
#
#
# def connect():
# 	pass
#
# def post(table, field, value, tag):
# 	pass
