import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from src import config
from easing_functions import *
import math

kit = ServoKit(channels=16)

class Control:

    def cservo(servo, cw, timeout, gpio_ch, throttle):

        if cw:
            throttle = -1 * throttle;
        else:
            throttle = 1 * throttle;

        kit.continuous_servo[servo.channel].throttle = throttle;
        if gpio_ch != 0:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(gpio_ch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            try:
                while True:
                    GPIO.wait_for_edge(gpio_ch, GPIO.FALLING)
                    time.sleep(0.02)
                    if not GPIO.input(gpio_ch):
                        break
            finally:
                GPIO.cleanup()
        else:
            time.sleep(timeout)

        kit.continuous_servo[servo.channel].throttle = 0;

    def rservo(servo, pos):
        kit.servo[servo.channel].set_pulse_width_range(servo.pulse_min, servo.pulse_max)
        Control.rtransition(servo, pos);
        servo.deg = pos;

    def rtransition(servo, out_deg):
        dur = abs(out_deg - servo.deg)
        dur = dur*(5*math.exp(1-dur/12) + 1.5)
        ease = QuadEaseInOut(servo.deg, out_deg, dur)
        i = 0;
        while i < dur:
            kit.servo[servo.channel].angle = ease.ease(i)
            i += 1;
            time.sleep(0.007)

    def stop(channel):
        kit.continuous_servo[channel].throttle = 0;