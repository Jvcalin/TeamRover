import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_pybadger.pygamer as pygamer

class MyMqtt:

    def __init__(self):
        # Get wifi details and more from a secrets.py file
        try:
            from secrets import secrets
        except ImportError:
            print("WiFi secrets are kept in secrets.py, please add them there!")
            raise

        esp32_cs = DigitalInOut(board.D13)
        esp32_ready = DigitalInOut(board.D11)
        esp32_reset = DigitalInOut(board.D12)

        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(self.spi, esp32_cs, esp32_ready, esp32_reset)

        if self.esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("ESP32 found and in idle mode")
        print("Firmware vers.", self.esp.firmware_version)
        print("MAC addr:", [hex(i) for i in self.esp.MAC_address])

        """Use below for Most Boards"""
        # status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)  # Uncomment for Most Boards

        #status_light = pygamer.pygamerNeoPixels

        self.wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(self.esp, secrets) #, status_light)

        ### Feeds ###
        self.status_feed = "roger/status/#"
        self.motor_cmd_feed = "roger/cmd/feather/motor"
        self.beep_cmd_feed = "roger/cmd/feather/beep"
        self.servo_cmd_feed = "roger/cmd/feather/servo"

        # Connect to WiFi
        print("Connecting to WiFi...")
        self.wifi.connect()
        print("Connected!")

        # Initialize MQTT interface with the esp interface
        MQTT.set_socket(socket, self.esp)

        # Set up a MiniMQTT Client
        self.mqtt_client = MQTT.MQTT(
            broker=secrets["mqtt_broker"],
            username=secrets["aio_username"],
            password=secrets["aio_key"],
        )

        # Setup the callback methods above
        self.mqtt_client.on_connect = self.connected
        self.mqtt_client.on_disconnect = self.disconnected
        self.mqtt_client.on_message = self.message

        # Connect the client to the MQTT broker.
        print("Connecting to MQTT...")
        self.mqtt_client.connect()



    ### Code ###

    # Define callback methods which are called when events occur
    # pylint: disable=unused-argument, redefined-outer-name
    def connected(self, client, userdata, flags, rc):
        # This function will be called when the client is connected
        # successfully to the broker.
        print("Connected to {0}! Listening for topic changes on {1}".format(secrets["mqtt_broker"], self.status_feed))
        # Subscribe to all changes on the onoff_feed.
        client.subscribe(self.status_feed)


    def disconnected(self, client, userdata, rc):
        # This method is called when the client is disconnected
        print("Disconnected from Roger!")


    def message(self, client, topic, message):
        # This method is called when a topic the client is subscribed to
        # has a new message.
        print("New message on topic {0}: {1}".format(topic, message))



    def checkMessages(self):
        # Poll the message queue
        self.mqtt_client.loop()

    def publishMessage(self, feed, message):
        print("Sending message to {0}: {1}".format(feed, message))
        self.mqtt_client.publish(feed, message)


"""
photocell_val = 0
while True:
    # Poll the message queue
    mqtt_client.loop()

    # Send a new message
    print("Sending photocell value: %d..." % photocell_val)
    mqtt_client.publish(photocell_feed, photocell_val)
    print("Sent!")
    photocell_val += 1
    time.sleep(1)
"""


"""
//Topics

//PUBLISH
//roger/status
//roger/status/feather
//roger/status/matrix
//roger/sensors/feather/proxf
//roger/sensors/feather/proxb
//roger/sensors/feather/proxl
//roger/sensors/feather/proxr
//roger/sensors/feather/motorspeed
//roger/sensors/feather/motoraction
//roger/sensors/feather/servohpos
//roger/sensors/feather/servovpos
//roger/sensors/feather/bump
//roger/sensors/feather/vib
//roger/sensors/feather/charging
//roger/sensors/feather/batt
//roger/sensors/feather/power

//SUBSCRIBE
//roger/cmd/feather/beep => "swoopup"
//roger/cmd/feather/motor => "forward"
//roger/cmd/feather/servo => "h,v"

//LOGGING
//cyke/telegraf/cmd
//cyke/telegraf/sensor
//cyke/telegraf/status

InfluxDb Format:
weather location="us",sensor="temp" temperature=78.1,humidity=23.1,description="wet",rain=true
"""