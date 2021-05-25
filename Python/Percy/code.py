import time
import oled
import wifimqtt as network
import motors

# import servos
# import sensors
#import motion

# Setup
myPrint = oled.MyPrint()
myMotors = motors.MyMotors(myPrint)
mqtt = network.MyMqtt("Percy", myPrint)

myPrint.print("Setup complete.")
# mqtt.publishMessage("roger/status/feather", "Susan has connected to Roger")


def quickLoop():
    pass


def slowLoop():
    mqtt.checkMessages()
    motors.tick()


# Main Loop
# Each loop iteration is 1 second
# The internal loop is 60 cycles
cyclesPerSecond = 60
cycleTime_ns = 1000000000/cyclesPerSecond
counter = 0
myPrint.print("Starting Loop...")
while True:
    t1 = time.monotonic_ns()
    for i in range(cyclesPerSecond):
        t = time.monotonic_ns()
        quickLoop()
        tt = time.monotonic_ns() - t
        if cycleTime_ns > tt:
            time.sleep((cycleTime_ns - tt)/1000000000)
    counter += 1
    slowLoop()
    myPrint.print("{}: {:.2f} s".format(counter,(time.monotonic_ns() - t1)/1000000000))