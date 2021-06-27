#import WiFiMqtt as network
import gamer_buttons as gamer
import time
import display

# Setup
# network.setupConnections()
# mqtt = network.MyMqtt()
# device = gamer.MyPyGamer(mqtt)
gamer.initialize()
print("Setup complete.")


# Main Loop
interval = 1/60
counter = 0
while True:
    """
    if counter > interval:
        mqtt.checkMessages()
        counter = 0
    else:
        counter = counter + 1
    """
    gamer.checkButtons()
    time.sleep(interval)  # Aiming for 60 cycles per second


