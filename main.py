from src import runner, control, interface, config
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

builder = runner.Builder();

builder.set_d1()

runner = builder.build()

def my_callback(e):
    sys.exit("STOPPED")
    print("STOP")

GPIO.add_event_detect(16, GPIO.RISING, callback=my_callback, bouncetime=300) 

print("Waiting for button...")

try:
    GPIO.wait_for_edge(21, GPIO.FALLING)
    print("Button hit!")
    print("Running sequence")
    runner.run();
except KeyboardInterrupt:
    GPIO.cleanup()
except SystemExit:
    print("STOPPED")
    GPIO.cleanup();
finally:
    GPIO.cleanup()