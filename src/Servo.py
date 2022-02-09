from src import control

class Servo:
    
    def __init__(self, name, deg, channel):
        self.name = name;
        self.channel = channel;
        self.deg = deg;

    def goto(self, pos):
        self.set(pos)

    def down(self):
        self.run(True, 10, False)

    def up(self):
        self.run(True, 10, False)

    def next(self):
        self.run(True, 10, False)

    def run(self, cw, timeout, stop):
        control.Control.cservo(self.channel, cw, timeout, stop)

    def set(self, pos):
        control.Control.rservo(self.channel, pos)



servos = {}

servos["d_arm"] = Servo("d_arm", 0, 0)
servos["d_cyl"] = Servo("d_cyl", 0, 0)
servos["d_mag"] = Servo("d_mag", 0, 0)

servos["b_arm"] = Servo("b_arm", 0, 0)
servos["b_mag"] = Servo("b_mag", 0, 0)
servos["dress_1"] = Servo("dress_1", 0, 0)
servos["dress_2"] = Servo("dress_2", 0, 0)