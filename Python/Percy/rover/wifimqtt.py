import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

import adafruit_minimqtt.adafruit_minimqtt as minimqtt

import broadcast


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


subscribes = {}
subscribe_funcs = {}
publishes = {}

MQTT = False

def initialize(myName, motorFunc):

    robotName = myName
    esp32_cs = DigitalInOut(board.D13)
    esp32_ready = DigitalInOut(board.D11)
    esp32_reset = DigitalInOut(board.D12)

    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

    if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
        broadcast.send("ESP32 found")

    """Use below for Most Boards"""
    status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)  # Uncomment for Most Boards

    wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

    ### Feeds ###
    publishes["status"] = "{}/status".format(robotName)
    subscribes["motor"] = "{}/cmd/motor".format(robotName)
    subscribe_funcs["{}/cmd/motor".format(robotName)] = motorFunc
    subscribes["beep"] = "{}/cmd/beep".format(robotName)
    subscribes["servo"] = "{}/cmd/servo".format(robotName)

    # Connect to WiFi
    broadcast.send("Connecting to WiFi...")
    try:
        wifi.connect()
        broadcast.send("Connected!")
    except:
        broadcast.send("Could not connect")
        raise


    # Initialize MQTT interface with the esp interface
    minimqtt.set_socket(socket, esp)

    # Set up a MiniMQTT Client
    global mqtt_client
    mqtt_client = minimqtt.MQTT(
        broker=secrets["mqtt_broker"],
        port=1883,
    )

    # Setup the callback methods above
    mqtt_client.on_connect = connected
    mqtt_client.on_disconnect = disconnected
    mqtt_client.on_message = message

    # Connect the client to the MQTT broker.
    broadcast.send(f"Connecting to MQTT Broker {secrets['mqtt_broker_name']}...")
    mqtt_client.connect()

    broadcast.send("MQTT initialized")
    global MQTT
    MQTT = True

### Code ###

# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    for item in subscribes:
        client.subscribe(subscribes[item])
        broadcast.send(f"Connected to {secrets['mqtt_broker']}! Listening for topic changes on {subscribes[item]}")

def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    broadcast.send("Disconnected from {}!".format(secrets["mqtt_broker_name"]))


def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    broadcast.send("New message on topic {0}: {1}".format(topic, message))
    subscribe_funcs[topic](message)

def checkMessages():
    # Poll the message queue
    mqtt_client.loop()


def publishMessage(message, feed=None):
    if feed == None:
        feed = publishes["status"]
    # self.print.print("Sending message to {0}: {1}".format(feed, message))
    mqtt_client.publish(feed, message)


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