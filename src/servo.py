from src import control
from src import config

class Servo:
    
    def __init__(self, name, channel): 
        self.name = name;
        self.channel = channel;

    def goto(self, pos):
        self.set(pos)

    def goto_meat_mag(self):
        print(config.meat_curr)
        config.meat_curr = (config.meat_curr + 1) % len(config.meat_degs)
        pos = config.degStates[f"meat{config.meat_curr}"]
        self.set(pos)

    def goto_veg_mag(self):
        config.veg_curr = (config.veg_curr + 1) % len(config.veg_degs)
        pos = config.degStates[f"veg{config.veg_curr}"]
        self.set(pos)

    def down(self):
        self.run(True, 2, False)

    def up(self):
        self.run(False, 2, False)

    def run(self, cw, timeout, stop):
        control.Control.cservo(self.channel, cw, timeout, stop)

    def set(self, pos):
        control.Control.rservo(self.channel, pos)

class SServo(Servo):
  def __init__(self, deg, *args):
      self.deg = deg;
      super(SServo,self).__init__(*args)

class CServo(Servo):
  def __init__(self, *args):
      super(CServo,self).__init__(*args)

servos = {}

servos["d_arm"] = SServo("d_arm", 0, 0)
servos["d_cyl"] = CServo("d_cyl", 0)

servos["b_arm"] = SServo("b_arm", 0, 0)
servos["b_mag"] = CServo("b_mag", 0)
servos["dress_1"] = CServo("dress_1", 0)
servos["dress_2"] = CServo("dress_2", 0)