from adafruit_servokit import ServoKit
from src import runner, control, interface, servo, max31855, ser_handler, config
from time import sleep
from threading import Thread
from easing_functions import *
import math
import numpy as np
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
kit = ServoKit(channels=16)

def run1(inn, out):
    t = abs(out - inn)
    dur = t*(5*math.exp(1-t/12) + 1.5)
    ease = QuadEaseInOut(inn, out, dur)
    i = 0;
    y = []
    while i < round(dur):
        y.append(ease.ease(i))
        i += 1;
    x = list(range(0, round(dur)))
    y2 = list(range(inn, out))
    x2 = list(range(0, len(y2)))
    fig, ax = plt.subplots()
    ax.scatter(x, y, 2**2, label="Mjukgjord lista")
    ax.set(xlim=(0, round(dur)), ylim=(inn, out))
    # ax.scatter(x2, y2, 2**2, label="Originallista")
    ax.legend()
    plt.xlabel('Index')
    plt.ylabel('Vinkel')
    plt.savefig("dummy_name2.png")

def plot():
    x = np.linspace(0,90,1000)

    # the function, which is y = x^2 here
    y = x*(5*np.exp(1-x/12) + 1.5)

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # plot the function
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(x,y, 'r')
    plt.savefig("test2.png")

def run2():
    kit.servo[1].angle = 0;
    sleep(3)
    kit.servo[1].angle = 90;
    sleep(2)
    kit.servo[1].angle = 0;

def run3(inn, out):
    t = abs(out - inn)
    dur = t*(5*math.exp(1-t/12) + 1.5)
    ease = QuadEaseInOut(inn, out, dur)
    i = 0;
    while i < round(dur):
        kit.servo[1].angle = ease.ease(i)
        i += 1;
        sleep(0.006)
    
    sleep(2)
    t = abs(inn - out)
    dur = t*(5*math.exp(1-t/12) + 1.5)
    ease = QuadEaseInOut(out, inn, dur)
    i = 0;
    while i < round(dur):
        kit.servo[1].angle = ease.ease(i)
        i += 1;
        sleep(0.006)
    
# bread_thread = Thread(target = run1).start()

def down():
    s = servo.CServo("d_cyl", 0)
    s.down()
def up():
    s = servo.CServo("d_cyl", 0)
    s.up()

def test2():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.LOW)
    sleep(0.5)

    GPIO.output(20, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(20, GPIO.LOW)
    sleep(0.5)

    # while True:
    #     if GPIO.input(config.pins['interface']['mag1_btn']):
    #     sleep(0.1)
    


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

# s = ser_handler.SerialHandler()

# sleep(4)

# s.write(785)

# s = servo.servos["d_arm"]
# s.goto(("mags",))

# sleep(2)

# s.goto(("heater",))
# sleep(2)
# s.goto(("mags",))


# plot()

run1(75, 100)
