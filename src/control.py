import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from src import config

kit = ServoKit(channels=16)

class Control:

    def cservo(sch, cw, timeout):
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
        kit.servo[servo.channel].angle = pos;