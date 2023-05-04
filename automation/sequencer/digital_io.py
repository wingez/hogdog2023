import threading
import time
from dataclasses import dataclass
from automation.sequencer.graph import Guard, Action

import RPi.GPIO as g

g.setmode(g.BCM)


@dataclass(frozen=True)
class Button:
    pin: int
    pull_up: bool = False
    inverted: bool = False


@dataclass
class LED:
    pin: int


class Outputs:
    led1 = LED(26)
    led2 = LED(16)
    led3 = LED(19)


g.setup(Outputs.led1.pin, g.OUT)
g.setup(Outputs.led2.pin, g.OUT)
g.setup(Outputs.led3.pin, g.OUT)


class Inputs:
    start = Button(21, pull_up=True, inverted=True)
    kveg = Button(7, pull_up=True, inverted=True)
    ketchup = Button(6, pull_up=True, inverted=True)
    mayo = Button(13, pull_up=True, inverted=True)
    load1 = Button(5, pull_up=True, inverted=True)
    load2 = Button(12, pull_up=True, inverted=True)
    probe_button1 = Button(17, pull_up=True, inverted=True)
    probe_button2 = Button(27, pull_up=True, inverted=True)


inputs = [Inputs.start, Inputs.kveg, Inputs.ketchup, Inputs.mayo, Inputs.load1, Inputs.load2, Inputs.probe_button1,
          Inputs.probe_button2]


for i in inputs:
    if i.pull_up:
        g.setup(i.pin, g.IN, pull_up_down=g.PUD_UP)
    else:
        g.setup(i.pin, g.IN)

input_state = {i: False for i in inputs}


class LEDState(Action):
    def __init__(self, led: LED, state: bool):
        super(LEDState, self).__init__()
        self.led = led
        self.state = state

    def execute(self):
        g.output(self.led.pin, self.state)


class ButtonPressed(Guard):
    def __init__(self, button: Button):
        super(ButtonPressed, self).__init__()
        self.button = button

    def evaluate(self) -> bool:
        return input_state[self.button]


def run_thread():
    while True:
        for i in inputs:
            result = g.input(i.pin)
            if i.inverted:
                result = not result

            input_state[i] = result

        time.sleep(0.01)


def start():
    thread = threading.Thread(target=run_thread, daemon=True)
    thread.start()

# thermometer = MAX31855(11, 10, 9)
