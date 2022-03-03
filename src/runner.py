import time 
from src import servo, config, heater
from threading import Thread

class Builder:

    def __init__(self):
        self.meat = True;
        self.d1 = False;
        self.d2 = False;

    def set_d1(self):
        self.d1 = True;
    def reset_d1(self):
        self.d1 = False;
    def set_d2(self):
        self.d2 = True;
    def reset_d2(self):
        self.d2 = False;
        
    def set_meat(self):
        self.meat = True;
    def reset_meat(self):
        self.meat = False;

    def build(self):
        dog = ["meat/veg", "dog_down", "dog_up", "dog_to_heater", "dog_down", "turn_on", "dog_up", "dog_to_bread", "dog_down"];
        bread = ["bread_to_dog", "to_dressing", "bread_to_dog"]
        if self.d1 and self.d2:
            bread[1] = "bread_to_d1"
            bread.insert(2, "bread_to_d2")
        elif self.d1 and not self.d2:
            bread[1] = "bread_to_d1"
        elif self.d2 and not self.d1:
            bread[1] = "bread_to_d2"
        
        if self.meat:
            dog[0] = "dog_to_meat"
        else:
            dog[0] = "dog_to_veg"

        b_seq = Sequence("b_seq", bread)
        d_seq = Sequence("d_seq", dog)

        return Runner([b_seq, d_seq])


class Runner:
    
    def __init__(self, seqs):
        self.seqs = seqs;

    def run(self):
        bread_thread = Thread(target = self.seqs[0].run)
        dog_thread = Thread(target = self.seqs[1].run)

        bread_thread.start()
        dog_thread.start()


class Sequence:

    def __init__(self, name, ops):
        self.name = name;
        self.ops = ops;

    def run(self):
        for op in self.ops:
            ops[op].run();


class Operation:

    def __init__(self, wait, fn, *args):
        self.fn = fn;
        self.args = args;
        self.wait = wait;

    def run(self):
        print(f"Running {self.fn}")
        if self.args:
            self.fn(self.args)
        else:
            self.fn();

        time.sleep(self.wait)

ops = {}

ops["dog_to_meat"] = Operation(0.5, servo.servos["d_arm"].goto_meat_mag)

ops["dog_to_veg"] = Operation(0.5, servo.servos["d_arm"].goto_veg_mag)

ops["dog_to_heater"]    = Operation(0.5, servo.servos["d_arm"].goto, "heater")
ops["dog_to_bread"]     = Operation(0.5, servo.servos["d_arm"].goto, "d_final")
ops["dog_down"]         = Operation(0.5, servo.servos["d_cyl"].down)
ops["dog_up"]           = Operation(0.5, servo.servos["d_cyl"].up)

#TODO ops["cook_dog"]         = Operation(Heater on, None)

ops["bread_to_mag"]     = Operation(2, servo.servos["b_arm"].goto, "b_mag")
ops["bread_to_d1"]      = Operation(2, servo.servos["b_arm"].goto, "d1")
ops["bread_to_d2"]      = Operation(2, servo.servos["b_arm"].goto, "d2") 
ops["bread_to_dog"]     = Operation(2, servo.servos["b_arm"].goto, "b_final")
ops["turn_on"]          = Operation(5, heater.Heater.turn_on)

# ops["dress1_push"]      = Operation(100, servo.servos["dress_1"].push, None)
# ops["dress1_release"]   = Operation(100, servo.servos["dress_1"].release, None)
# ops["dress2_push"]      = Operation(100, servo.servos["dress_2"].push, None)
# ops["dress2_release"]   = Operation(100, servo.servos["dress_2"].release, None)