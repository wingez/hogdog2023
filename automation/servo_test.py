from adafruit_servokit import ServoKit
import time

lower_servo = 0
upper_servo = 6

arm_servo = 9



#def servo_update_ang(ang, channel):
#    kit.servo[channel].angle = ang
kit = ServoKit(channels=16)
kit.servo[6].actuation_range = 170 #Upper servo MAX
kit.servo[6].actuation_range = 60 # Lower min?

from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
from adafruit_servokit import ServoKit
import time
import RPi.GPIO as g

from thermocoupler import MAX31855


class Outputs:
    led1 = 26
    led2 = 16
    led3 = 19


class Inputs:
    start = 21
    kveg = 7
    ketchup = 6
    mayo = 13
    load1 = 5
    load2 = 12
    probe_button1 = 17
    probe_button2 = 27


thermometer = MAX31855(11, 10, 9)

g.setmode(g.BCM)

g.setup(Outputs.led1, g.OUT)
g.setup(Outputs.led2, g.OUT)
g.setup(Outputs.led3, g.OUT)

g.setup(Inputs.start, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.kveg, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.ketchup, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.mayo, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.load1, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.load2, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.probe_button1, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.probe_button2, g.IN, pull_up_down=g.PUD_UP)

kit = ServoKit(channels=16)


def callback_probe_button1_RISE(channel):
    # time.sleep(0.1)

    print("RISING edge detected on 24")


def callback_probe_button1_FALL(channel):
    # time.sleep(0.1)
    print("hello")
    print("FALLING edge detected on 24")


def callback_probe_button2_RISE(channel):
    print("RISING edge detected on 23")


def callback_probe_button2_FALL(channel):
    # time.sleep(0.1)
    print("world")

    print("FALLING edge detected on 23")


# when a falling edge is detected on port 24/23, regardless of whatever
# else is happening in the program, the function my_callback will be run
g.add_event_detect(Inputs.probe_button1, g.RISING, callback=callback_probe_button1_RISE, bouncetime=300)
#g.add_event_detect(Inputs.probe_button1, g.FALLING, callback=callback_probe_button1_FALL, bouncetime=300)

#g.add_event_detect(Inputs.probe_button2, g.RISING, callback=callback_probe_button2_RISE, bouncetime=300)
g.add_event_detect(Inputs.probe_button2, g.FALLING, callback=callback_probe_button2_FALL, bouncetime=300)

if __name__ == '__main__':
    import time

    prev = True

    while True:
        i = g.input(Inputs.probe_button1)
        if i != prev:
            print("transisiton", i)

        prev = i
        time.sleep(0.001)


    time.sleep(99999)
#
# if __name__ == '__main__':
#     x = range(50, 160, 5)
#     for i in reversed(range(50,160,5)):
#         kit.servo[0].angle = int(i)
#         time.sleep(0.1)
#
#     #kit.servo[4].angle = 60
#     #kit.servo[0].angle = 50
#
#     #kit.continuous_servo[4].throttle = 0.3
#     #time.sleep(2)
#     #kit.continuous_servo[4].throttle = 0