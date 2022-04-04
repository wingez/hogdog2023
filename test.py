from adafruit_servokit import ServoKit
from src import runner, control, interface, servo, max31855, ser_handler
from time import sleep
from threading import Thread
from easing_functions import *
import math
import RPi.GPIO as GPIO
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

def down():
    s = servo.CServo("d_cyl", 0)
    s.down()
def up():
    s = servo.CServo("d_cyl", 0)
    s.up()

def test2():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        print("Waiting for trigger")
        while True:
            GPIO.wait_for_edge(26, GPIO.FALLING)
            print("TRIGGAD")
            sleep(0.2)
            if not GPIO.input(26):
                break
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        GPIO.cleanup()
    finally:
        print("klar")
        GPIO.cleanup()


# thermocouple = max31855.max31855.MAX31855(8, 11, 9, "c")
# try:
#     while True:
#         sleep(1)
#         print(thermocouple.get())
# except KeyboardInterrupt:
#     print("Keyboard Interrupt")
#     thermocouple.cleanup() 
# finally:
#     thermocouple.cleanup() 

s = ser_handler.SerialHandler()

sleep(4)

s.write(785)