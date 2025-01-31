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


@dataclass(frozen=True)
class LED:
    pin: int


class Outputs:
    led1 = LED(26)
    led2 = LED(16)
    led3 = LED(19)
    heat = LED(23)


g.setup(Outputs.led1.pin, g.OUT)
g.setup(Outputs.led2.pin, g.OUT)
g.setup(Outputs.led3.pin, g.OUT)

output_state = {i: False for i in [
    Outputs.led1,
    Outputs.led2,
    Outputs.led3,
]}


def set_output(led: LED, state: bool):
    output_state[led] = state
    g.output(led.pin, state)


class Inputs:
    start = Button(21, pull_up=True, inverted=True)
    kveg = Button(7, pull_up=True, inverted=True)
    ketchup = Button(6, pull_up=True, inverted=True)
    mayo = Button(13, pull_up=True, inverted=True)
    load1 = Button(5, pull_up=True, inverted=True)
    load2 = Button(12, pull_up=True, inverted=True)
    arm_top = Button(17, pull_up=True, inverted=True)
    arm_bot = Button(27, pull_up=True, inverted=True)


inputs = [Inputs.start, Inputs.kveg, Inputs.ketchup, Inputs.mayo, Inputs.load1, Inputs.load2, Inputs.arm_top,
          Inputs.arm_bot]

for i in inputs:
    if i.pull_up:
        g.setup(i.pin, g.IN, pull_up_down=g.PUD_UP)
    else:
        g.setup(i.pin, g.IN)

input_state = {i: False for i in inputs}


class LEDSet(Action):
    def __init__(self, led: LED, state: bool):
        super(LEDSet, self).__init__()
        self.led = led
        self.state = state

    def execute(self):
        set_output(self.led, self.state)


class LEDState(Guard):
    def __init__(self, led: LED, state: bool):
        super(LEDState, self).__init__()
        self.led = led
        self.state = state

    def evaluate(self) -> bool:
        return output_state[self.led] == self.state


class ButtonPressed(Guard):
    def __init__(self, button: Button):
        super(ButtonPressed, self).__init__()
        self.button = button

    def evaluate(self) -> bool:
        return input_state[self.button]


class ButtonNotPressed(ButtonPressed):
    def evaluate(self) -> bool:
        return not ButtonPressed.evaluate(self)


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
