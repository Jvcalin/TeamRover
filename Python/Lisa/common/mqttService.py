import paho.mqtt.client as mqtt
import time

class RoverMqttSubscription:
    def __init__(self, topic, callback):
        self.topic = topic
        self.callBack = callback


class RoverMqtt:

    def __init__(self, name, subscriptions, host="192.168.86.25", port=1883):
        self.name = name
        self.thisMqtt = mqtt.Client(name, False)  # clean sessions =false so subsriptions are maintained and messages are saved if disconnected
        self.thisMqtt.on_message = self.on_message
        self.thisMqtt.on_connect = self.on_connect
        self.thisMqtt.connect(host, port, keepalive=60)
        # self.thisMqtt.subscribe("roger/cmd/#", 2)
        # self.thisMqtt.subscribe("roger/sensors/#", 2)
        self.subscription = subscriptions
        for s in subscriptions:
            self.thisMqtt.subscribe(s.topic, 2)
        self.thisMqtt.loop_start()
        self.thisMqtt.publish(self.name + "/status", self.name + " starting", 2, True)

    def __del__(self):
        # body of destructor
        self.closemqtt()
        

    def closemqtt(self):
        self.thisMqtt.publish("roger/status", self.name + " stopping", 2, True)
        self.thisMqtt.loop_stop()
        

    def on_message(self, client, userdata, message):
        print("got message")
        print(client)
        print(userdata)
        print(message.payload.decode("utf-8"))
        print(message.topic)
        print(message.retain)
        print(message.qos) 
        for s in self.subscription:
            if self.matchroute(s.topic, message.topic):
                s.callBack(message.payload.decode("utf-8"))
                break

    
    def matchroute(self, topic1, topic2):
        # routes is robotname/messagetype/device/item/subitem
        top1 = topic1.split("/")
        top2 = topic2.split("/")
        i = 0
        while i < len(top1) and i < len(top2):
            if top1[i] == top2[i]:
                i += 1
                continue
            else:
                if top1[i] == "#" or top2[i] == "#":
                    return True # wildcard
                else:
                    return False # no match
        if len(top1) == len(top2):
            return True # complete match
        else:
            return False # incomplete match

    def publish(self, topic, message):
        self.thisMqtt.publish(topic, message, 2, True)
        print("Published " + message + " to " + topic)

    # TODO do something with the message
    # if cmd, call to execute cmd
    # if sensor, update state vars for device

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))


    # client.subscribe("roger/cmd/#", 2)
    # client.subscribe("roger/sensors/#", 2)


"""
def subDo(message):
    print("subscribe " + message)

sub1 = RoverMqttSubscription("roger/cmd/#", lambda x : subDo(x))
sub2 = RoverMqttSubscription("roger/sensors/#", lambda x : subDo(x))

subs = [sub1, sub2]

this = RoverMqtt("myMqtt", subs)

for i in range(10):
    time.sleep(5)

this.closemqtt()


"""
#QOS 0 – Only Once
#QOS 1 – At Least Once
#QOS 2 – Only Once
#
#
#Topics
#roger/status
#roger/status/feather
#roger/status/matrix

#roger/cmd/feather/beep => "swoopup"
#roger/cmd/feather/action => "forward"
#roger/cmd/feather/servo => "h,v"
#roger/cmd/presence/publish  -- publish the presence array

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

#roger/presence/proxarray -- contains the proxarray


#Examples
#roger/cmd/matrix/led/roundinacircle = 3 (times)
#roger/cmd/matrix/led/rainbow => 3 (times)
#roger/cmd/matrix/
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


#LOGGING
#patty/telegraf/cmd
#patty/telegraf/sensor
#patty/telegraf/status

#InfluxDb Format:
#weather location="us",sensor="temp" temperature=78.1,humidity=23.1,description="wet",rain=true 