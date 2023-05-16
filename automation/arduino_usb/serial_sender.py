#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1) #ACMx
    ser.reset_input_buffer()
    i_val = 79.00
    while True:
        ser.write(b" " + str(i_val).encode('utf-8') + b"\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
            #i_val = i_val + 1
        i_val = input("Enter new kHz request: ")

#oenauhsaonteuh