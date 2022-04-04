import time
from src import servo, config, heater
from threading import Thread

class Builder:

    def __init__(self):
        self.meat = True;
        self.d1 = False;
        self.d2 = False;

    def toggle_d1(self, status):
        temp = status
        time.sleep(0.2)
        if temp == status:
            self.d1 = status;
    def set_d2(self):
        self.d2 = True;
    def reset_d2(self):
        self.d2 = False;
        
    def set_meat(self):
        self.meat = True;
    def reset_meat(self):
        self.meat = False;

    def build(self):
        dog = ["dog_to_mags", "meat/veg", "dog_down", "dog_up", "dog_to_heater", "dog_down", "turn_on", "dog_up", "dog_to_bread", "dog_down"];
        bread = ["bread_to_dog", "dressing", "bread_to_dog"]

        if self.d1 and self.d2:
            bread[1] = "bread_to_d1"
            bread.insert(2, "dress1")
            bread.insert(3, "bread_to_d2")
            bread.insert(4, "dress2")
        elif self.d1 and not self.d2:
            bread[1] = "bread_to_d1"
            bread.insert(2, "dress1")
        elif self.d2 and not self.d1:
            bread[1] = "bread_to_d2"
            bread.insert(2, "dress2")
        
        if self.meat:
            dog[1] = "dog_to_meat"
            config.meat_curr -= 1
    
        else:
            dog[1] = "dog_to_veg"
            config.veg_curr -= 1

        b_seq = Sequence("b_seq", bread)
        d_seq = Sequence("d_seq", dog)
        fin_seq = Sequence("fin_seq", ["dog_final", "bread_final", "dog_up", "dog_to_mags"])

        return Runner([b_seq, d_seq, fin_seq])


class Runner:
    
    def __init__(self, seqs):
        self.seqs = seqs;
        self.running = False;

    def run(self):
        bread_thread = Thread(target = self.seqs[0].run)
        dog_thread = Thread(target = self.seqs[1].run)
        final_thread = Thread(target = self.seqs[2].run_sync)

        self.running = True
        bread_thread.start()
        dog_thread.start()

        bread_thread.join()
        dog_thread.join()

        final_thread.start()
        final_thread.join()

        self.running = False



class Sequence:

    def __init__(self, name, ops):
        self.name = name;
        self.ops = ops;

    def run(self):
        for op in self.ops:
            op_th = Thread(target = ops[op].run)
            op_th.start()
            op_th.join()

    def run_sync(self):
        op1 = Thread(target = ops["dog_final"].run)
        op2 = Thread(target = ops["bread_final"].run)
        op3 = Thread(target = ops["dog_up"].run)
        op4 = Thread(target = ops["dog_to_mags"].run)
        op1.start()
        op2.start()
        op1.join()
        op2.join()
        op3.start()
        op3.join()
        op4.start()
        op4.join()
        print(f"FINISHED")


class Operation:

    def __init__(self, wait, fn, *args):
        self.fn = fn;
        self.args = args;
        self.wait = wait;
        self.post = False;

    def run(self):
        print(f"OPERATION STARTED: {self.fn} --- {self.args}")
        if self.args:
            self.fn(self.args)
        else:
            self.fn();

        time.sleep(self.wait)


ops = {}

ops["dog_to_meat"] = Operation(0.1, servo.servos["d_arm"].goto_meat_mag)

ops["dog_to_veg"] = Operation(0.1, servo.servos["d_arm"].goto_veg_mag)

ops["dog_to_mags"] = Operation(0.1, servo.servos["d_arm"].goto, "mags")

ops["dog_to_heater"]    = Operation(0.1, servo.servos["d_arm"].goto, "heater")
ops["dog_to_bread"]     = Operation(0.1, servo.servos["d_arm"].goto, "d_final")
ops["dog_final"]        = Operation(0.1, servo.servos["d_arm"].goto, "d_takeoff")
ops["dog_down"]         = Operation(0.1, servo.servos["d_cyl"].down)
ops["dog_up"]           = Operation(0.1, servo.servos["d_cyl"].up)

#TODO ops["cook_dog"]         = Operation(Heater on, None)

ops["bread_to_mag"]     = Operation(0.1, servo.servos["b_arm"].goto, "b_mag")
ops["bread_to_d1"]      = Operation(0.1, servo.servos["b_arm"].goto, "d1")
ops["bread_to_d2"]      = Operation(0.1, servo.servos["b_arm"].goto, "d2")
ops["bread_to_dog"]     = Operation(0.1, servo.servos["b_arm"].goto, "b_final")
ops["bread_final"]      = Operation(0.1, servo.servos["b_arm"].goto, "b_takeoff")
ops["turn_on"]          = Operation(1, heater.Heater.turn_on)

ops["dress1"]           = Operation(1, servo.servos["dress_1"].dress)
ops["dress2"]           = Operation(1, servo.servos["dress_2"].dress)