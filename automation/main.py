
print("hello world!")
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)


from adafruit_servokit import ServoKit
print("hello world!")


kit = ServoKit(channels=16)

TOP=20
BOTTOM=21


GPIO.setup(TOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOTTOM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# This is a sample Python script.



while True:


    print("starting moving down")
    kit.continuous_servo[7].throttle=-0.1
    while GPIO.input(BOTTOM)==1 :
        pass

    print("moving up")
    kit.continuous_servo[7].throttle = 0.1
    while GPIO.input(TOP) == 1:
        pass

    print("cycle")


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
