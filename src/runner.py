import time 
from src import servo
from src import config

class Runner:
    
    def __init__(self, name, seqs):
        self.name = name;
        self.seqs = seqs;

    def run(self):
        for seq in self.seqs:
            seq.run();



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

ops[f"dog_to_meat"] = Operation(2, servo.servos["d_arm"].goto_meat_mag)

ops[f"dog_to_veg"] = Operation(2, servo.servos["d_arm"].goto_veg_mag)

ops["dog_to_heater"]    = Operation(2, servo.servos["d_arm"].goto, "heater")
ops["dog_to_bread"]     = Operation(2, servo.servos["d_arm"].goto, "d_final")
ops["dog_down"]         = Operation(2, servo.servos["d_cyl"].down)
ops["dog_up"]           = Operation(2, servo.servos["d_cyl"].up)

#TODO ops["cook_dog"]         = Operation(Heater on, None)

ops["bread_to_mag"]     = Operation(100, servo.servos["b_arm"].goto, "b_mag")
ops["bread_to_d1"]      = Operation(100, servo.servos["b_arm"].goto, "d1")
ops["bread_to_d2"]      = Operation(100, servo.servos["b_arm"].goto, "d2") 
ops["bread_to_dog"]     = Operation(100, servo.servos["b_arm"].goto, "b_final")

# ops["dress1_push"]      = Operation(100, servo.servos["dress_1"].push, None)
# ops["dress1_release"]   = Operation(100, servo.servos["dress_1"].release, None)
# ops["dress2_push"]      = Operation(100, servo.servos["dress_2"].push, None)
# ops["dress2_release"]   = Operation(100, servo.servos["dress_2"].release, None)



dog_ops = ["dog_to_meat", "dog_down", "dog_up", "dog_to_heater", "dog_down", "cook_dog", "dog_up", "dog_to_bread", "dog_down", "dog_up", "next_dog"]

dog_seq = Sequence("dog_seq", dog_ops)

bread_ops1 = ["bread_to_mag", "next_bread", "bread_to_d1", "bread_to_dog"]
bread_ops2 = ["bread_to_mag", "next_bread", "bread_to_d2", "bread_to_dog"]
