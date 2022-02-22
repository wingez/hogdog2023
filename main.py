from src import runner, control, interface, config
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Waiting for button...")

try:
    GPIO.wait_for_edge(21, GPIO.FALLING)
    print("Button hit!")
    print("Running sequence")
    runner.dog_seq.run()
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()