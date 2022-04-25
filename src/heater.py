from src import max31855
from threading import Thread
from time import sleep

class Heater:

    def __init__(self): 
        self.freq = 123

    def turn_on():
        print("heating")
        Heater.thermo_read();
    
    def thermo_read():
        thermocouple = max31855.max31855.MAX31855(8, 11, 9, "c")
        while True:
            temp = thermocouple.get()
            print(temp)
            if temp >= 23:
                print("heating done")
                break;
            sleep(0.5)