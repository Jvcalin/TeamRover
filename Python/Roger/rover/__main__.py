import rover as rvr
import time

# The Rover Loop
# Read and publish Matrix One Sensor Info
# Get cmds to control RGB Pixels


roger = rvr.Rover()


while True:
    if roger.tick():
        break
    time.sleep(0.02)
    #roger.readSensors()
    #roger.checkEvents()
    #_mqtt.checkEvents()
    #_triggers.check()

#check inbox for messages
#readings



#close mqtt
#mqtt.closemqtt()

#def subCallback():
#   pass
