import WiFiMqtt as network
import gamer_buttons as gamer
import time

# Setup
# network.setupConnections()
mqtt = network.MyMqtt()
device = gamer.MyPyGamer(mqtt)
print("Setup complete.")
mqtt.publishMessage("roger/status/feather","Susan has connected to Roger")

# Main Loop
interval = 5
counter = 0
while True:
    if counter > interval:
        mqtt.checkMessages()
        counter = 0
    else:
        counter = counter + 1
    device.checkButtons()
    time.sleep(0.2)