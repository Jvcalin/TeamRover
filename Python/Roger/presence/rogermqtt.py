import paho.mqtt.client as mqtt
import time

#Topics
#roger/status
#roger/status/feather
#roger/status/matrix

#roger/cmd/feather/beep => "swoopup"
#roger/cmd/feather/action => "forward"
#roger/cmd/feather/servo => "h,v"
##roger/sensors/feather/proxf
#roger/sensors/feather/proxb
#roger/sensors/feather/proxl
#roger/sensors/feather/proxr
#roger/sensors/feather/motor/speed
#roger/sensors/feather/motor/action
#roger/sensors/feather/servo/h
#roger/sensors/feather/servo/v
#roger/sensors/feather/bump
#roger/sensors/feather/vib
#roger/sensors/feather/charging
#roger/sensors/feather/batt
#roger/sensors/feather/power

#roger/cmd/matrix/led/roundinacircle = 3 (times)
#roger/cmd/matrix/led/rainbow => 3 (times)
#roger/sensors/matrix/imu/accel
#roger/sensors/matrix/imu/gyro
#roger/sensors/matrix/imu/orientation

#roger/event/me/forward
#roger/event/me/spinleft
#roger/event/me/spinright
#roger/event/me/backward
#roger/event/me/tipforward
#roger/event/me/tipbackward
#roger/event/me/tipleft
#roger/event/me/tipright
#roger/event/me/brake
#roger/event/me/bump



theRover = None

def initializemqtt(rover):
	theRover = rover
	rogerMqtt = mqtt.client("RogerMQTT_Pi",False) #clean sessions =false so subsriptions are maintained and messages are saved if disconnected
	rogerMqtt.on_message = on_message
	rogerMqtt.on_connect = on_connect
	rogerMqtt.connect("192.169.1.25", 1883)
	rogerMqtt.subscribe("roger/cmd/#", 2)
	rogerMqtt.subscribe("roger/sensors/#", 2)
	rogerMqtt.loop_start()
	rogerMqtt.publish("roger/status", "presence loop starting", 2, true)
	
def closemqtt():
	rogerMqtt.publish("roger/status", "presence loop stopping", 2, true)
	rogerMqtt.loop_stop()

def on_message(client, userdata, message):
	print("got message")
	print(client)
	print(userdata)
	print(message)

	#TODO do something with the message
	#if cmd, call to execute cmd
	#if sensor, update state vars for device

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	#client.subscribe("roger/cmd/#", 2)
	#client.subscribe("roger/sensors/#", 2)

def getroute(path):
	#routes is robotname/messagetype/device/item/subitem
	route = path.split("/")
	return route

#Client = mqtt.client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
#Client.connect(host, port=1883, keepalive=60, bind_address="")
#Client.publish(topic, payload=None, qos=0, retain=False)
#Client.subscribe(topic, qos=0)
#Client.on_message=function_you_define
#Client.loop_start()
#Client.loop_stop() 
#time.sleep(4) # wait


#def on_message(client, userdata, message):
#    print("message received " ,str(message.payload.decode("utf-8")))
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)
#def on_log(client, userdata, level, buf):
#    print("log: ",buf)
#client.on_log=on_log
#on_subscribe(client, userdata, mid, granted_qos)

#QOS 0 – Only Once
#QOS 1 – At Least Once
#QOS 2 – Only Once
#
#

