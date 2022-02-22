import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

class Control:

    def cservo(sch, cw, timeout, stop):
        tm = timeout;

        timeout = time.time() + timeout;

        if cw:
            while time.time() < timeout:
                if stop:
                    break
                Control.test(tm);
        else:
            while time.time() < timeout:
                if stop:
                    break
                Control.test(tm);

    def rservo(sch, pos):
        #TODO kör servo sch till deg
        return None

    def test(timeout):
        p = GPIO.PWM(17, 100)
        p.start(4)
        p.ChangeDutyCycle(4)
        time.sleep(timeout)
        p.ChangeDutyCycle(1.5) # may need to be adjusted
        GPIO.cleanup();

    def testccw(timeout):
        p = GPIO.PWM(17, 100)
        p.start(4)
        p.ChangeDutyCycle(20.5)
        time.sleep(timeout)
        p.ChangeDutyCycle(1.5) # may need to be adjusted
        GPIO.cleanup();