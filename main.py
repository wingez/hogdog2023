from src import runner, control, interface, servo
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def stop_all(e):
    print("stop")
    servo.Servo.stop();
    sys.exit()
GPIO.add_event_detect(16, GPIO.RISING, callback=stop_all, bouncetime=300)

builder = runner.Builder();

builder.set_d1()

runner = builder.build()

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