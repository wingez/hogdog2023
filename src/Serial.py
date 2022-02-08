# lsusb to check device name
#dmesg | grep "tty" to find port name
import serial
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

class Serial:

    def write(msg):
        ser.write(msg)