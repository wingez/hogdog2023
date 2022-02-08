import time
from config import servos

class Sequencer:
    
    def __init__(self, name, seqs):
        self.name = name;
        self.seqs = seqs;



class Sequence:

    def __init__(self, name, ops, wait):
        self.name = name;
        self.ops = ops;
        self.wait = wait;

    def run(self):
        for op in self.ops:
            op.run();

        time.sleep(self.wait())



class Operation:

    def __init__(self, fn, *args):
        self.fn = fn;
        self.args = args;

    def run(self):
        self.fn(self.args);