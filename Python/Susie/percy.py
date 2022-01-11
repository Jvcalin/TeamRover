import robot
# colors CRIMSON rgb(220,20,60) #DC143C


def apply_dir(message, op1, op2):
    return message[0] * op1, message[1] * op2, message[2]


class Percy(robot.Robot):

    def __init__(self, mqtt, refresh_func):
        super().__init__(mqtt, refresh_func)
        self.mqtt = mqtt
        self.feeds = {"motor": "percy/cmd/motor", "servo": "percy/cmd/servo"}
        self.name = "Percy"
        self.counter = 0  # how long the button is pressed
        self.prev_dir = 0
        self.prev_a = False
        self.prev_b = False
        self.speed = 1

    def tick(self):
        if self.mode == "motor":
            if not self.a and self.prev_a: # button up
                self.speed += 1
                if self.speed > 2:
                    self.speed = 2
            self.prev_a = self.a

            if not self.b and self.prev_b: # button up
                self.speed -= 1
                if self.speed < 1:
                    self.speed = 1
            self.prev_b = self.b

            if self.prev_dir == self.direction:
                if self.direction == 0:
                    pass
                else:
                    self.counter += 1
                    # print(self.counter)
                    if self.counter > 60:
                        self.fire_command(self.direction)
            else:  # a change in direction
                # print(self.prev_dir, " - ", self.direction)
                if self.prev_dir != 0: # don't fire if going from neutral to direction
                    self.fire_command(self.prev_dir)
                self.prev_dir = self.direction
                self.refresh()
        else:
            self.refresh()


    def fire_command(self, cmd):
        # print("fire")
        if self.mode == "motor":
            message = (self.speed, self.speed, self.counter)
            if cmd > 0:
                if cmd == 1:
                    message = apply_dir(message, 1, 1)
                elif cmd == 2:
                    message = apply_dir(message, 1, 0.75)
                elif cmd == 3:
                    message = apply_dir(message, 1, -1)
                elif cmd == 4:
                    message = apply_dir(message, -1, -0.75)
                elif cmd == 5:
                    message = apply_dir(message, -1, -1)
                elif cmd == 6:
                    message = apply_dir(message, -0.75, -1)
                elif cmd == 7:
                    message = apply_dir(message, -1, 1)
                elif cmd == 8:
                    message = apply_dir(message, 0.75, 1)
                else:
                    message = apply_dir(message, 0, 0)
                self.mqtt.publish_message(self.feeds[self.mode], message)
        self.counter = 0