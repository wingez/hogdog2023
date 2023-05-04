from adafruit_servokit import ServoKit
import time

#def servo_update_ang(ang, channel):
#    kit.servo[channel].angle = ang
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 170 #Upper servo MAX
kit.servo[0].actuation_range = 60 # Lower min?


if __name__ == '__main__':
    x = range(50, 160, 5)
    for i in reversed(range(50,160,5)):
        kit.servo[0].angle = int(i)
        time.sleep(0.1)

    #kit.servo[4].angle = 60
    #kit.servo[0].angle = 50

    #kit.continuous_servo[4].throttle = 0.3
    #time.sleep(2)
    #kit.continuous_servo[4].throttle = 0