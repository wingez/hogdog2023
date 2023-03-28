from adafruit_servokit import ServoKit
import time

#def servo_update_ang(ang, channel):
#    kit.servo[channel].angle = ang

if __name__ == '__main__':
    kit = ServoKit(channels=16)
    kit.servo[0].angle = 0
    kit.continuous_servo[4].throttle = 0.3
    time.sleep(2)
    kit.continuous_servo[4].throttle = 0