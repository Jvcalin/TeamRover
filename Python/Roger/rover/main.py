from rover import Rover
import time

# The Rover Loop
# Read and publish Matrix One Sensor Info
# Get cmds to control RGB Pixels


roger = Rover()


while True:
	#roger.readSensors()
	#roger.checkEvents()
	#_mqtt.checkEvents()
	#_triggers.check()
	if roger.tick():
		break
	time.sleep(0.1)

#check inbox for messages
#readings



#close mqtt
#mqtt.closemqtt()

#def subCallback():
#	pass
