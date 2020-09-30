"""
https://orientdb.com/docs/2.2.x/PyOrient.html
https://orientdb.com/docs/2.2.x/PyOrient-Client.html
"""

import pyorient
import pyorient.ogm

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("admin", "admin_passwd")

# Check Database
if client.db_exists("tinkerhome"):
   # Open Database
   client.db_open("tinkerhome", "admin", "admin_passwd")

#Direct SQL to DB
# for sensor in pollen_sensors:
#      client.command(
#       "INSERT INTO PollenSensor "
#       "('device_id', 'read_time', 'read') "
#       "VALUES('%s', '%s', %s')"
#       % (sensor.get_id()
#          time.now(),
#          sensor.get_data()))

# client.query(<query>, <limit>, <fetch-plan>)
data = client.query("SELECT FROM Sensors "
                    "WHERE sensorType = 'Pollen'",
                    100)
data = client.query("SELECT FROM Sensors "
                    "WHERE room = 'bedroom'",
                    100, "*:-1")

# client.record_create(<cluster_id>, <data>)
# data = {
#    @<class>: {
#       <property>: <value>
#    }
# }

# event = {
#    @DoorSecurityEvent: {
#       "time_start": timestamp_start,
#       "time_end": timestamp_end,
#       "webcam_file": "/path/to/file.ogg,
#       "doorbell": True,
#       "knock": False,
#       "open": True,
#       "open_type": "InnerLock"
#    },
# }
# client.record_create(cluster_id, event)

# client.record_delete(<cluster-id>, <record-id>)
# client.record_delete(cluster_id, record.__rid)

# client.record_load(<rid>, <fetch-plan>, <callback>)
# Process Data
# def compile_data(client, rid_array):
#
#    # Initialize Variable
#    data = {}
#
#    # Iterate through Record ID's
#    for rid in rid_array:
#
#       # Log Data
#       data[rid] = client.record_load(rid)
#
#    # Return Data
#    return data

# client.record_update(<record-id>, <data>, <version>)
# data = {
#    @<class>: {
#       <property>: <value>
#    }
# }
# Fetch Grocery List
eggs = client.query(
   "SELECT FROM ShoppingList "
   "WHERE type = 'grocery'"
   "AND item = 'eggs'")

data = {
   "@ShoppingList": {
      "quantity": 24
   }
}
client.record_update(eggs._rid, data, eggs._version)

