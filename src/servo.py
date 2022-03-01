from src import control
from src import config

class Servo:
    
    def __init__(self, name, channel): 
        self.name = name;
        self.channel = channel;

    def goto(self, pos):
        print(pos)
        self.set(config.degStates[pos[0]])

    def goto_meat_mag(self):
        config.meat_curr = (config.meat_curr + 1) % len(config.meat_degs)
        pos = config.degStates[f"meat{config.meat_curr}"]
        self.set(pos)

    def goto_veg_mag(self):
        config.veg_curr = (config.veg_curr + 1) % len(config.veg_degs)
        pos = config.degStates[f"veg{config.veg_curr}"]
        self.set(pos)

    def down(self):
        self.run(True, 2)

    def up(self):
        self.run(False, 2)

    def run(self, cw, timeout):
        control.Control.cservo(self.channel, cw, timeout)

    def set(self, pos):
        control.Control.rservo(self, pos)

class SServo(Servo):
  def __init__(self, deg, pulse_min, pulse_max, *args):
      self.deg = deg;
      self.pulse_min = pulse_min;
      self.pulse_max = pulse_max;
      super(SServo,self).__init__(*args)

class CServo(Servo):
  def __init__(self, *args):
      super(CServo,self).__init__(*args)

servos = {}

servos["d_arm"] = SServo(0, 430, 2290,"d_arm",  1)
servos["d_cyl"] = CServo("d_cyl", 0)

servos["b_arm"] = SServo(0, 430, 2290, "b_arm", 2)
servos["b_mag"] = CServo("b_mag", 100)
servos["dress_1"] = CServo("dress_1", 100)
servos["dress_2"] = CServo("dress_2", 100)