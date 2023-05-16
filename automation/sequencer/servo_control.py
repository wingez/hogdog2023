import threading
from typing import Tuple, List, Dict

from adafruit_servokit import ServoKit
import time
from datetime import datetime, timedelta
from automation.sequencer.graph import Guard, Action
import atexit
from automation.sequencer import sigmoid_gen

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

latest_servo_angles = {lower_servo: 49, upper_servo: 13}


def write_angle(servo: int, angle: int):
    kit.servo[servo].angle = angle
    latest_servo_angles[servo] = angle

    global last_move_time
    last_move_time = datetime.now()


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
        write_angle(self.servo, self.angle)


class SmoothServoAngle(Action):
    def __init__(self, servo: int, angle: int):
        super(SmoothServoAngle, self).__init__()
        self.servo = servo
        self.angle = angle

    def execute(self):
        global last_move_time
        last_move_time = datetime.now()

        start_angle = latest_servo_angles[self.servo]
        end_angle = self.angle

        steps = int(abs(start_angle - end_angle) / 25 * 100)

        angles = sigmoid_gen.servo_smoothed(start_angle, end_angle, steps)

        list_of_angles_to_write[self.servo].extend(angles)


class ServoSpeed(Action):
    def __init__(self, servo: int, speed: float):
        super(ServoSpeed, self).__init__()
        self.servo, self.speed = servo, speed

    def execute(self):
        kit.continuous_servo[self.servo].throttle = self.speed


list_of_angles_to_write: Dict[int, List[int]] = {upper_servo: [], lower_servo: []}


def run_thread():
    while True:

        for servo in list_of_angles_to_write:
            angles = list_of_angles_to_write[servo]
            if len(angles) > 0:
                angle = angles.pop(0)
                write_angle(servo, angle)

        time.sleep(0.01)


def start():
    thread = threading.Thread(target=run_thread, daemon=True)
    thread.start()
