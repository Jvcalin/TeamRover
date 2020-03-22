# Adafruit MiniMQTT Pub/Sub Example
# Written by Tony DiCola for Adafruit Industries
# Modified by Brent Rubell for Adafruit Industries
import time
import board
import busio
from digitalio import DigitalInOut
import neopixel_spi
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_minimqtt import MQTT
import gamer_buttons as pygamer

class MyMqtt:

    def __init__(self):
        # Get wifi details and more from a secrets.py file
        try:
            from secrets import secrets
        except ImportError:
            print("WiFi secrets are kept in secrets.py, please add them there!")
            raise

        # If you are using a board with pre-defined ESP32 Pins:
        #esp32_cs = DigitalInOut(board.ESP_CS)
        #esp32_ready = DigitalInOut(board.ESP_BUSY)
        #esp32_reset = DigitalInOut(board.ESP_RESET)

        # If you have an ItsyBitsy Airlift:
        esp32_cs = DigitalInOut(board.D13)
        esp32_ready = DigitalInOut(board.D11)
        esp32_reset = DigitalInOut(board.D12)

        # If you have an externally connected ESP32:
        # esp32_cs = DigitalInOut(board.D9)
        # esp32_ready = DigitalInOut(board.D10)
        # esp32_reset = DigitalInOut(board.D5)

        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(self.spi, esp32_cs, esp32_ready, esp32_reset)
        """Use below for Most Boards"""
        # status_light = neopixel.NeoPixel(
        #    board.NEOPIXEL, 1, brightness=0.2
        #)  # Uncomment for Most Boards
        """Uncomment below for ItsyBitsy M4"""
        # status_light = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
        # Uncomment below for an externally defined RGB LED
        # import adafruit_rgbled
        # from adafruit_esp32spi import PWMOut
        # RED_LED = PWMOut.PWMOut(esp, 26)
        # GREEN_LED = PWMOut.PWMOut(esp, 27)
        # BLUE_LED = PWMOut.PWMOut(esp, 25)
        # status_light = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)

        #status_light = pygamer.pygamerNeoPixels
        self.wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(self.esp, secrets) #, status_light)

        ### Feeds ###

        # Setup a feed named 'photocell' for publishing to a feed
        #photocell_feed = secrets["aio_username"] + "/feeds/photocell"


        # Setup a feed named 'onoff' for subscribing to changes
        #onoff_feed = secrets["aio_username"] + "/feeds/onoff"

        self.status_feed = "roger/status/#"
        self.motor_cmd_feed = "roger/cmd/feather/motor"
        self.beep_cmd_feed = "roger/cmd/feather/beep"

        # Connect to WiFi
        self.wifi.connect()

        # Set up a MiniMQTT Client
        self.mqtt_client = MQTT(
            socket,
            broker="192.168.1.25",
            port=1883,
            network_manager=self.wifi,
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
        print("Connected to Roger! Listening for topic changes on %s" % self.status_feed)
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
"""