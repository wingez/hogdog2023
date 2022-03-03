from adafruit_servokit import ServoKit
from time import sleep
from threading import Thread
from easing_functions import *
import math
kit = ServoKit(channels=16)

def run1(inn, out):
    dur = abs(out - inn)
    print(dur)
    dur = dur*(5*math.exp(1-dur/10) + 1)
    print(dur)
    ease = QuadEaseInOut(inn, out, dur)
    i = 0;
    while i < dur:
        kit.servo[1].angle = ease.ease(i)
        i += 1;
        sleep(0.005)

def run2():
    kit.continuous_servo[0].throttle = 1;
    sleep(3)
    kit.continuous_servo[0].throttle = -1;
    sleep(2)
    kit.continuous_servo[0].throttle = 0;

    
# bread_thread = Thread(target = run1).start()

run1(0, 180);
run1(180, 0);
run1(0, 15);
run1(15, 0);
run1(0, 90);
run1(90, 0);