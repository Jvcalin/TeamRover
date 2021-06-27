import robot
# colors CRIMSON rgb(220,20,60) #DC143C


class Percy(robot.Robot):

    def __init__(self):
        super.__init__()
        self.feeds = {"motor": "percy/cmd/motor", "servo": "percy/cmd/servo"}
        self.name = "Percy"
        self.counter = 0  # how long the button is pressed
        self.prev_dir = 0
        self.prev_a = False
        self.prev_b = False
        self.speed = 1

    def tick(self):
        if not self.a and self.prev_a: # button up
            self.speed += 1
        self.prev_a = self.a

        if not self.b and self.prev_b: # button up
            self.speed -= 1
        self.prev_b = self.b

        if self.direction == 0:
            if self.prev_dir == 0:
                pass
            else:
                self.counter = 0
                self.fire_command()
        else:
            if self.prev_dir == self.direction:
                self.counter += 1
            else:
                self.counter = 0
                self.fire_command()
        self.prev_dir = self.direction

    def fire_command(self):
        if self.mode == "motor":
            message = (self.speed,self.speed,self.counter)
            if self.direction == 1:
                message = self.applydir(message, 1, 1)
            elif self.direction == 2:
                message = self.applydir(message, 1, 0.75)
            elif self.direction == 3:
                message = self.applydir(message, 1, -1)
            elif self.direction == 4:
                message = self.applydir(message, -1, -0.75)
            elif self.direction == 5:
                message = self.applydir(message, -1, -1)
            elif self.direction == 6:
                message = self.applydir(message, -0.75, -1)
            elif self.direction == 7:
                message = self.applydir(message, -1, 1)
            elif self.direction == 8:
                message = self.applydir(message, 0.75, 1)
            else:
                message = self.applydir(message, 0, 0)
        else:
            message = ""
        self.mqtt.publish(self.feeds[self.mode], message)

    def applydir(self, message, op1, op2):
        return message[0] * op1, message[1] * op2, message[2]

