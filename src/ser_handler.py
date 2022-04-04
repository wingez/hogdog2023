import serial
import time
from threading import Thread

class SerialHandler:

    def __init__(self):
        self.baud = 9600;
        self.port = "/dev/ttyUSB0"
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        self.ser.reset_input_buffer()


    def read(self):
        input = "";
        while not input:
            input = self.ser.readline()
            print(input)
            time.sleep(0.2)
        return input.decode("utf-8")

    def write(self, msg):
        print("msg sent")
        self.ser.write(f"{msg}\n".encode("utf-8"))