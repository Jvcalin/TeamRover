from adafruit_pybadger import pygamer
import display
import robot
import percy
import roger
import wifi_mqtt

def refresh():
    display.show(device.button.up, device.button.down, device.button.left, device.button.right, robot.name, "motors", robot.mode == "motor", "servos", robot.mode == "servo")

device = pygamer.pygamer
myMqtt = wifi_mqtt.MyMqtt("susie", device.pixels)
percy = percy.Percy(myMqtt, refresh)
roger = roger.Roger(myMqtt, refresh)

robot = percy

start_button = False
select_button = False



def check_buttons():
    global robot
    global start_button
    global select_button
    if robot != None:
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
            start_button = True
        else:
            if start_button:
                start_button = False
                toggle_robot()

        if device.button.select:
            select_button = True
        else:
            if select_button:
                select_button = False
                select_button = False
                robot.toggle_mode()


def toggle_robot():
    global robot
    if robot is None:
        robot = percy
    elif robot.name == "Percy":
        robot = roger
    else:
        robot = percy

