import paho.mqtt.client as mqtt
import time




def initializemqtt():
	rogerMqtt = mqtt.client("RogerMQTT_Pi")
	rogerMqtt.connect("192.169.1.25", 1883
	


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

