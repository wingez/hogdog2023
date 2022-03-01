import serial
import time

ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
ser.reset_input_buffer()

class SerialHandler:

    def __init__(self):
        self.baud = 57600;
        self.ser = serial.Serial('/dev/ttyACM0', self.baud, timeout=1)
        self.ser.reset_input_buffer()


    def read(self):
        input = "";
        while not input:
            input = ser.readline().strip()
        return input.decode("utf-8")

    def write(self, msg):
        print("msg sent")
        ser.write(f"{msg}\n".encode("utf-8"))


test = SerialHandler()

test.write("test");
print(test.read());