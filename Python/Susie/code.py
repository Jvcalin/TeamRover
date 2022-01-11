#import WiFiMqtt as network
import gamer
import time
import display

# Setup
# network.setupConnections()
# mqtt = network.MyMqtt()
# device = gamer.MyPyGamer(mqtt)
# gamer.initialize()
print("Setup complete.")
display.show(False, False, False, False, "Percy", "Motors", True, "Servos", False)


# Main Loop
interval = 1/10
counter = 0
while True:
    """
    if counter > interval:
        mqtt.checkMessages()
        counter = 0
    else:
        counter = counter + 1
    """
    gamer.check_buttons()
    time.sleep(interval)

