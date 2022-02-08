import Control
from config import degStates

class Servo:
    
    def __init__(self, name, deg):
        self.name = name;
        self.deg = deg;

    def goto(self, pos):
        self.set(self.name, degStates[pos])

    def down(self):
        self.set(0)

    def up(self):
        self.set(0)

    def next(self):
        self.set(0)

    def set(self, deg, time):
        Control.servo(self.name, deg, time)