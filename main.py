from src import runner, control, servo, interface
import RPi.GPIO as GPIO
import sys
from threading import Thread
import time

builder1 = runner.Builder();
interface1 = interface.Interface(builder1)
runner1 = None
print("Waiting for button...")

def start(e):
    GPIO.remove_event_detect(21)
    interface1.go()
    runner1 = builder1.build()   
    print("Button hit!")
    print("Running sequence")
    run_th = Thread(target = runner1.run)
    run_th.start()
    print("Thread started")
    run_th.join()
    print("Thread stopped")
    interface1.check()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        GPIO.add_event_detect(21, GPIO.RISING, callback=start, bouncetime=300)
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    finally:
        GPIO.cleanup() 

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
interface1.check()
print("test")
try:
    GPIO.add_event_detect(21, GPIO.RISING, callback=start, bouncetime=300)
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
finally:
    GPIO.cleanup() 