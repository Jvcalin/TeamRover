if __name__ == '__main__':
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))  # Make common library available
    print(sys.path)
    print(str(Path(__file__)))

import rover as rvr
import time

# The Rover Loop
# Read and publish Matrix One Sensor Info
# Get cmds to control RGB Pixels
print("starting main")

roger = rvr.Rover()


while True:
    if roger.tick():
        break
    # time.sleep(0.002)
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
