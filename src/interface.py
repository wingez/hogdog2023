import RPi.GPIO as GPIO
from src import config
import time
GPIO.setmode(GPIO.BCM)

MEAT_PIN=13
D1_PIN=17
D2_PIN=22
START_PIN=21
START_LED_PIN=24
MAG_1_FILL_PIN=6
MAG_2_FILL_PIN=9
MAG_1_FILL_LED_PIN=12
MAG_2_FILL_LED_PIN=25
HEATER_LED_PIN=8



class Interface: 

    def __init__(self, builder):
        self.ready_togo=False
        self.builder = builder

        GPIO.setup(MEAT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(D1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(D2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(START_LED_PIN, GPIO.OUT)
        GPIO.setup(MAG_1_FILL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(MAG_2_FILL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(MAG_1_FILL_LED_PIN, GPIO.OUT)
        GPIO.setup(MAG_2_FILL_LED_PIN, GPIO.OUT)
        GPIO.setup(HEATER_LED_PIN, GPIO.OUT)
        
    def check(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.add_event_detect(MAG_1_FILL_PIN, GPIO.RISING, callback=self.fyllt1 , bouncetime=300)
        GPIO.add_event_detect(MAG_2_FILL_PIN, GPIO.RISING, callback=self.fyllt2 , bouncetime=300)

        while not self.ready_togo:
                
            if GPIO.input(MEAT_PIN):
                self.builder.set_meat()
            else:
                self.builder.reset_meat()

            if config.meat_curr <= 0 and self.builder.meat:
                GPIO.output(MAG_1_FILL_LED_PIN, 1)
                print("mag 1 needs refill")
                print("mag 1 low (LED_ON)")

            if config.veg_curr <= 0 and not self.builder.meat:
                GPIO.output(MAG_2_FILL_LED_PIN, 1)
                print("mag 2 needs refill")
                print("mag 2 low (LED_ON)")

            if ((config.meat_curr > 0 and self.builder.meat) or (config.veg_curr > 0 and not self.builder.meat)):# and not running :
                self.ready_togo = True
                self.start_led_on()
            time.sleep(0.1)

        if GPIO.input(D1_PIN):
            self.builder.set_d1()
        else:
            self.builder.reset_d1()

        if GPIO.input(D2_PIN):
            self.builder.set_d2()
        else:
            self.builder.reset_d2()

    def fyllt1(self, e):
        GPIO.output(MAG_1_FILL_LED_PIN , 0)
        config.meat_curr = 10
        
        print("mag 1 full")
        print("mag 1 (LED_OFF)")

    def fyllt2(self, e):
        GPIO.output(MAG_2_FILL_LED_PIN , 0)
        config.veg_curr = 5
        
        print("mag 2 full")
        print("mag 2 (LED_OFF)")

    def start_led_on(self):
        GPIO.output(START_LED_PIN , 1)

    def start_led_off(self):
        GPIO.output(START_LED_PIN , 0)


    def go(self):
        if self.ready_togo:
            self.start_led_off()
            self.ready_togo = False

        



