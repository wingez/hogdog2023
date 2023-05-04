from adafruit_servokit import ServoKit
import time
from datetime import datetime, timedelta
from automation.sequencer.graph import Guard, Action
import atexit

lower_servo = 0
upper_servo = 6

arm_servo = 9

move_time_s = 3
last_move_time = datetime.now()

arm_down = -1
arm_up = 1

# def servo_update_ang(ang, channel):
#    kit.servo[channel].angle = ang
kit = ServoKit(channels=16)


def stop_continuous():
    # Stop all continuous_servo servo
    kit.continuous_servo[arm_servo].throttle = 0


stop_continuous()

# Stop all servos on exit
atexit.register(stop_continuous)


class ServoIdle(Guard):
    def __init__(self, servo: int):
        super(ServoIdle, self).__init__()
        self.servo = servo

    def evaluate(self) -> bool:
        return datetime.now() - last_move_time > timedelta(seconds=move_time_s)


class ServoAngle(Action):
    def __init__(self, servo: int, angle: int):
        super(ServoAngle, self).__init__()
        self.servo = servo
        self.angle = angle

    def execute(self):
        global last_move_time
        last_move_time = datetime.now()
        kit.servo[self.servo].angle = self.angle


class ServoSpeed(Action):
    def __init__(self, servo: int, speed: float):
        super(ServoSpeed, self).__init__()
        self.servo, self.speed = servo, speed

    def execute(self):
        kit.continuous_servo[self.servo].throttle = self.speed
