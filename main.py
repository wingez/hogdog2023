from asyncio.windows_events import NULL
from hogdog.src import interface
from src import runner, control, servo
import RPi.GPIO as GPIO
import sys
from threading import Thread
import time

builder1 = runner.Builder();
builder1.set_d1()
builder1.set_d2()
interface1 = interface()
runner1 = NULL
print("Waiting for button...")

def start(e):
    GPIO.remove_event_detect(21)
    runner1 = builder1.build()   
    print("Button hit!")
    print("Running sequence")
    run_th = Thread(target = runner1.run)
    run_th.start()
    print("Thread started")
    run_th.join()
    print("Thread stopped")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        GPIO.add_event_detect(21, GPIO.RISING, callback=start, bouncetime=300)
        while True:
            time.sleep(0.1)
            # INTERFACE THREAD
            check_th = Thread(target = interface1.check)
            check_th.start()
            interface1.check()
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    finally:
        GPIO.cleanup() 

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