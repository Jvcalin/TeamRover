import WiFiMqtt as network
import gamer_buttons as gamer
import time
import display

# Setup
# network.setupConnections()
mqtt = network.MyMqtt()
device = gamer.MyPyGamer(mqtt)
print("Setup complete.")
mqtt.publishMessage("roger/status/feather","Susan has connected to Roger")

# Main Loop
interval = 60
counter = 0
while True:
    if counter > interval:
        mqtt.checkMessages()
        display.draw_screen("Roger", "motors", False, False, False, False)
        counter = 0
    else:
        counter = counter + 1
    device.checkButtons()
    time.sleep(0.2)