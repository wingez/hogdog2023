import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from src import config
from easing_functions import *
import math

kit = ServoKit(channels=16)

class Control:

    def cservo(sch, cw, timeout, stop):
        stop = False;
        tm = timeout;

        timeout = time.time() + timeout;

        if cw:
            throttle = -1;
        else:
            throttle = 1;

        kit.continuous_servo[sch].throttle = throttle;

        while time.time() < timeout:
            if stop:
                break

        kit.continuous_servo[sch].throttle = 0;

    def rservo(servo, pos):
        kit.servo[servo.channel].set_pulse_width_range(servo.pulse_min, servo.pulse_max)
        Control.rtransition(servo, pos);
        servo.deg = pos;

    def rtransition(servo, out_deg):
        dur = abs(out_deg - servo.deg)
        dur = dur*(5*math.exp(1-dur/12) + 1)
        ease = QuadEaseInOut(servo.deg, out_deg, dur)
        i = 0;
        while i < dur:
            kit.servo[servo.channel].angle = ease.ease(i)
            i += 1;
            time.sleep(0.005)