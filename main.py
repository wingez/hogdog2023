from src import runner, control, servo, interface, config
import RPi.GPIO as GPIO
import sys
from threading import Thread
import time

builder1 = runner.Builder();
interface1 = interface.Interface(builder1)
runner1 = None
servo.Servo.stop()
builder1.init()
while True:
    check = Thread(target = interface1.check)
    check.start()
    check.join()
    print("Button hit!")
    runner1 = builder1.build()
    print("Running!")
    run_th = Thread(target = runner1.run)
    # run_th = Thread(target = runner1.test)
    run_th.start()
    print("Thread started!")
    run_th.join()
    print("Thread stopped!")