import threading
import time

from automation.sequencer.graph import Guard
from automation.thermocoupler import MAX31855

thermometer = MAX31855(11, 10, 9)

last_reading = 20.0


class TempAbove(Guard):
    def __init__(self, tmp: float):
        super(TempAbove, self).__init__()
        self.tmp = tmp

    def evaluate(self) -> bool:
        return last_reading > self.tmp


def run_thread():
    global last_reading
    while True:
        last_reading = thermometer.get()
        print("Thermometer: ", last_reading)
        time.sleep(2)


def start():
    thread = threading.Thread(target=run_thread, daemon=True)
    thread.start()
