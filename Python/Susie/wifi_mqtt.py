import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

import adafruit_minimqtt.adafruit_minimqtt as MQTT

# import adafruit_pybadger.pygamer as pygamer

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


class MyMqtt:

    def __init__(self, name, status_light):
        esp32_cs = DigitalInOut(board.D13)
        esp32_ready = DigitalInOut(board.D11)
        esp32_reset = DigitalInOut(board.D12)

        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(self.spi, esp32_cs, esp32_ready, esp32_reset)

        if self.esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
            print("ESP32 found and in idle mode")
        print("Firmware vers.", self.esp.firmware_version)
        print("MAC addr:", [hex(i) for i in self.esp.MAC_address])

        self.status_light = status_light  # pygamer.pygamerNeoPixels

        self.wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(self.esp, secrets, self.status_light)

        ### Feeds ###
        self.name = name
        self.status_feed = "{0}/status/#".format(name)

        # Connect to WiFi
        print("Connecting to WiFi...")
        self.wifi.connect()
        print("Connected!")

        # Initialize MQTT interface with the esp interface
        MQTT.set_socket(socket, self.esp)

        # Set up a MiniMQTT Client
        self.mqtt_client = MQTT.MQTT(
            broker=secrets["mqtt_broker"],
            port=1883,
        )

        # Setup the callback methods above
        self.mqtt_client.on_connect = self.connected
        self.mqtt_client.on_disconnect = self.disconnected
        self.mqtt_client.on_message = self.message

        # Connect the client to the MQTT broker.
        print("Connecting to MQTT...Broker {0}".format(secrets["mqtt_broker_name"]))
        self.mqtt_client.connect()
        print("Connected to broker {0}".format(secrets["mqtt_broker_name"]))
        self.publishMessage(self.status_feed, "{0} has connected to {1}".format(name, secrets["mqtt_broker_name"]))

    # Define callback methods which are called when events occur
    # pylint: disable=unused-argument, redefined-outer-name
    def connected(self, client, userdata, flags, rc):
        # This function will be called when the client is connected
        # successfully to the broker.
        print("Connected to {0}!".format(secrets["mqtt_broker"]))
        # client.subscribe(self.status_feed)

    def disconnected(self, client, userdata, rc):
        # This method is called when the client is disconnected
        print("Disconnected!")

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


