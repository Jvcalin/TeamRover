from adafruit_pybadger import pygamer
import display
import robot
import percy
import roger
import wifi_mqtt

robot = None
device = pygamer.pygamer
myMqtt = wifi_mqtt.MyMqtt("susie", device.pygamerNeoPixels)
percy = percy.Percy(myMqtt)
roger = roger.Roger(myMqtt)

def check_buttons():
    if robot != None:
        display.show(device.button.up, device.button.down, device.button.left, device.button.right, robot.name, "motors", robot.mode == "motor", "servos", robot.mode == "servo")
        if device.button.up and device.button.left:
            robot.upleft()
        elif device.button.up and device.button.right:
            robot.upright()
        elif device.button.down and device.button.left:
            robot.downleft()
        elif device.button.down and device.button.right:
            robot.downright()
        elif device.button.left:
            robot.left()
        elif device.button.right:
            robot.right()
        elif device.button.up:
            robot.up()
        elif device.button.down:
            robot.down()
        else:
            robot.center()

        if device.button.a:
            robot.a_press()
        else:
            robot.a_up()

        if device.button.b:
            robot.b_press()
        else:
            robot.b_up()

        if device.button.start:
            robot.start_press()
        else:
            robot.start_up()

        if device.button.select:
            robot.select_press()
        else:
            robot.select_up()

def toggle_robot():
    global robot
    if robot is None:
        robot = percy

    if robot.name == "Percy":
        robot = roger
    else:
        robot = percy



