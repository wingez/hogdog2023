import serial
import time

class SerialHandler:

    def __init__(self):
        self.baud = 57600;
        self.ser = serial.Serial('/dev/ttyACM0', self.baud, timeout=1)
        self.ser.reset_input_buffer()


    def read(self):
        while True:
            input = ser.read()
            print (input.decode("utf-8"))


ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
ser.reset_input_buffer()

while True:
    ser.write("Hej fran RPI\n".encode("utf-8"))
    line = ser.readline().rstrip()
    print(line)
    time.sleep(1)
