import time
import broadcast
import sys

try:
    from adafruit_crickit import crickit
    MOTORS = True
    broadcast.send("Motors initialized")
except ValueError:
    MOTORS = False
    broadcast.send("Motors not found")

MAX_SPEED = 2.0
COUNTDOWN = 60

# make two variables for the motors to make code shorter to type
if MOTORS:
    mleft = crickit.dc_motor_1
    mright = crickit.dc_motor_2

lspeed = 0.0   # speed values ->  -2 to 2
rspeed = 0.0

countdown = 0



def tick():
    if MOTORS:
        global countdown
        global mleft
        global mright
        global lspeed
        global rspeed
        if countdown > 0:  # every move command will expire after countdown goes to 0
            countdown -= 1
        else:
            lspeed = 0.0
            rspeed = 0.0
        mleft.throttle = lspeed / MAX_SPEED  # throttle: 1 = full speed, 0 is stop, 0.5 is half speed, neg is rev
        mright.throttle = rspeed / MAX_SPEED

def move(left=0.0, right=0.0, duration=COUNTDOWN):
    if MOTORS:
        global countdown
        global lspeed
        global rspeed
        broadcast.send("Move: {:.2f}.{:.2f}".format(left, right))
        if left > MAX_SPEED:
            lspeed = MAX_SPEED
        elif left < (MAX_SPEED * -1):
            lspeed = MAX_SPEED * -1
        else:
            lspeed = left
        if right > MAX_SPEED:
            rspeed = MAX_SPEED
        elif right < (MAX_SPEED * -1):
            rspeed = MAX_SPEED * -1
        else:
            rspeed = right

        countdown = duration

def stop():
    global countdown
    broadcast.send("stop")
    lspeed = 0.0
    rspeed = 0.0
    mleft.throttle = 0.0
    mright.throttle = 0.0
    countdown = 0


def receive_command(payload):
    params = payload.strip().lower().split(',')
    print(params)
    cmd = params[0].strip()
    leftspeed = float(params[1].strip())
    rightspeed = float(params[2].strip())
    duration = float(params[3].strip())

    move(leftspeed, rightspeed, duration)

def is_moving_forward():
    return lspeed > 0 and rspeed > 0

def is_moving_backward():
    return lspeed < 0 and rspeed < 0