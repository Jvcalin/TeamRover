import presence.rover
import presence.rogermqtt as mqtt


#this is the main loop
STOP = False  #this will become true when a STOP file is placed in the inbox

#initialize mqtt
roger = Rover()
mqtt.initializemqtt(roger)

while not STOP:
	roger.readSensors()
	roger.checkEvents()
	

#check inbox for messages
#readings



#close mqtt
mqtt.closemqtt()
