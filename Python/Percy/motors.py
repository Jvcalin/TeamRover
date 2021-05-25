import time
from adafruit_crickit import crickit

MAX_SPEED = 2
COUNTDOWN = 3

class MyMotors:

    def __init__(self, myPrint):
        # make two variables for the motors to make code shorter to type
        self.mleft = crickit.dc_motor_1
        self.mright = crickit.dc_motor_2

        self.print = myPrint

        self.lspeed = 0 #speed values ->  -2 to 2
        self.rspeed = 0

        self.countdown = 0

    def tick(self):
        if countdown > 0: # every move command will expire after countdown goes to 0
            countdown -= 1
        else:
            self.lspeed = 0
            self.rspeed = 0
        self.mleft.throttle = lspeed / MAX_SPEED  #throttle: 1 = full speed, 0 is stop, 0.5 is half speed, neg is rev
        self.mright.throttle = rspeed / MAX_SPEED

    def move(self, left, right):
        if left > MAX_SPEED:
            self.lspeed = MAX_SPEED
        elif left < (MAX_SPEED * -1):
            self.lspeed = MAX_SPEED * -1
        else:
            self.lspeed = left
        if right > MAX_SPEED:
            self.rspeed = MAX_SPEED
        elif right < (MAX_SPEED * -1):
            self.rspeed = MAX_SPEED * -1
        else:
            self.rspeed = right
        self.countdown = COUNTDOWN

