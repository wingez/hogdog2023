from adafruit_servokit import ServoKit
from time import sleep
from threading import Thread
kit = ServoKit(channels=16)

def run1():
    kit.servo[1].angle = 0;
    sleep(2)
    kit.servo[1].angle = 35;
    sleep(2)
    kit.servo[1].angle = 90;
    sleep(2)
    kit.servo[1].angle = 180;
    sleep(2)

def run2():
    kit.continuous_servo[0].throttle = 1;
    sleep(3)
    kit.continuous_servo[0].throttle = -1;
    sleep(2)
    kit.continuous_servo[0].throttle = 0;

    
bread_thread = Thread(target = run1).start()
dog_thread = Thread(target = run2).start()