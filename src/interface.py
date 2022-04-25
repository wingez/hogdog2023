import RPi.GPIO as GPIO
from src import config
import time
GPIO.setmode(GPIO.BCM)

MEAT_PIN=config.pins['interface']['meat']
D1_PIN=config.pins['interface']['d1']
D2_PIN=config.pins['interface']['d2']
START_PIN=config.pins['interface']['s_btn']
START_LED_PIN=config.pins['interface']['s_led']
MAG_1_FILL_PIN=config.pins['interface']['mag1_btn']
MAG_2_FILL_PIN=config.pins['interface']['mag2_btn']
MAG_1_FILL_LED_PIN=config.pins['interface']['mag1_led']
MAG_2_FILL_LED_PIN=config.pins['interface']['mag2_led']
HEATER_LED_PIN=config.pins['interface']['heater_led']


class Interface: 

    def __init__(self, builder):
        self.ready_togo=False
        self.run = False
        self.builder = builder
        self.meat_refill = False
        self.veg_refill = False
        
    def fyllt1(self, e):
        GPIO.output(MAG_1_FILL_LED_PIN , GPIO.LOW)
        config.meat_curr = 9
        self.meat_refill = False
        print("mag 1 full")
        print("mag 1 (LED_OFF)")

    def fyllt2(self, e):
        GPIO.output(MAG_2_FILL_LED_PIN , GPIO.LOW)
        config.veg_curr = 4
        self.veg_refill = False
        print("mag 2 full")
        print("mag 2 (LED_OFF)")

    def check(self):
        GPIO.setmode(GPIO.BCM)
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
        
        GPIO.output(MAG_1_FILL_LED_PIN , GPIO.LOW)
        GPIO.output(MAG_2_FILL_LED_PIN , GPIO.LOW)
        GPIO.add_event_detect(START_PIN, GPIO.RISING, callback=self.go, bouncetime=300)

        self.run = False
        self.ready_togo = False
        
        self.start_led_off()

        while not self.run:

            if config.meat_curr < 0 and not self.meat_refill:
                GPIO.output(MAG_1_FILL_LED_PIN, GPIO.HIGH)
                GPIO.add_event_detect(MAG_1_FILL_PIN, GPIO.RISING, callback=self.fyllt1, bouncetime=300)
                print("mag 1 needs refill")
                print("mag 1 low (LED_ON)")
                self.meat_refill = True

            if config.veg_curr < 0 and not self.veg_refill:
                GPIO.output(MAG_2_FILL_LED_PIN, GPIO.HIGH)
                GPIO.add_event_detect(MAG_2_FILL_PIN, GPIO.RISING, callback=self.fyllt2, bouncetime=300)
                print("mag 2 needs refill")
                print("mag 2 low (LED_ON)")
                self.veg_refill = True
            
            if not GPIO.input(MEAT_PIN):
                self.builder.set_meat()
            else:
                self.builder.reset_meat()

            if ((config.meat_curr >= 0 and self.builder.meat) or (config.veg_curr >= 0 and not self.builder.meat)):# and not running :
                self.ready_togo = True
                print("READY")
                self.start_led_on()
            else:
                self.start_led_off()
                self.ready_togo = False

            time.sleep(0.2)

        if not GPIO.input(D1_PIN):
            self.builder.set_d1()
        else:
            self.builder.reset_d1()

        if not GPIO.input(D2_PIN):
            self.builder.set_d2()
        else:
            self.builder.reset_d2()

        GPIO.remove_event_detect(START_PIN)
            
        self.veg_refill = False
        self.meat_refill = False

        return True

    def start_led_on(self):
        GPIO.output(START_LED_PIN , GPIO.HIGH)

    def start_led_off(self):
        GPIO.output(START_LED_PIN , GPIO.LOW)

    def go(self, e):
        time.sleep(0.1)
        if GPIO.input(START_PIN):
            if self.ready_togo and not self.run:
                self.run = True
                self.start_led_off()