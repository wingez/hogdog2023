import time
from config import servos

class Runner:
    
    def __init__(self, name, seqs):
        self.name = name;
        self.seqs = seqs;



class Sequence:

    def __init__(self, name, ops):
        self.name = name;
        self.ops = ops;

    def run(self):
        for op in self.ops:
            op.run();



class Operation:

    def __init__(self, wait, fn, *args):
        self.fn = fn;
        self.args = args;
        self.wait = wait;

    def run(self):
        self.fn(self.args);

        time.sleep(self.wait)