import RPi.GPIO as GPIO
from src import config
GPIO.setmode(GPIO.BCM)

MEAT_PIN=17
D1_PIN=13
D2_PIN=22
START_PIN=23
START_LED_PIN=24
MAG_1_FILL_PIN=10
MAG_2_FILL_PIN=9
MAG_1_FILL_LED_PIN=11
MAG_2_FILL_LED_PIN=25
HEATER_LED_PIN=8



class Interface: 

    def __init__(self, builder):
        self.mag1_ammo=10
        self.mag2_ammo=5
        self.ready_togo=True
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


        GPIO.add_event_detect(MEAT_PIN, GPIO.BOTH,   callback=lambda x: self.builder.toggle_meat(GPIO.input(MEAT_PIN)) , bouncetime=500)          #korv

        GPIO.add_event_detect(D1_PIN, GPIO.BOTH,   callback=lambda x: self.builder.toggle_d1(GPIO.input(D1_PIN)) , bouncetime=100)           #dressing 1

        GPIO.add_event_detect(D2_PIN, GPIO.BOTH,   callback=self.builder.set_d2 , bouncetime=300)          #dressing2    

        GPIO.add_event_detect(START_PIN, GPIO.RISING, callback=self.go , bouncetime=300)   #startknapp

        GPIO.add_event_detect(MAG_1_FILL_PIN, GPIO.RISING, callback=self.fyllt1 , bouncetime=300)       # fyll 1

        GPIO.add_event_detect(MAG_2_FILL_PIN, GPIO.RISING, callback=self.fyllt2 , bouncetime=300)       # fyll 2
        

    def check(self):

        if config.meat_curr <= 0:
            GPIO.output(MAG_1_FILL_LED_PIN, 1)
            print("mag 1 needs refill")
            print("mag 1 low (LED_ON)")


        if config.veg_curr <= 0:
            GPIO.output(MAG_2_FILL_LED_PIN, 1)
            print("mag 2 needs refill")
            print("mag 2 low (LED_ON)")

        #if #heater_on:
         #  GPIO.output(HEATER_LED_PIN, 1)
         #  print("heater on (LED)")

        else:
            GPIO.output(HEATER_LED_PIN, 0)
            print("heater off (LED)")
            
            

        if ((config.meat_curr > 0 and self.builder.meat) or (config.veg_curr > 0 and not self.builder.meat)):# and not running :
            self.ready_togo = True
            self.start_led_on()
            print("Ready to go")
        


    def fyllt1(self):
        GPIO.output(MAG_1_FILL_LED_PIN , 0)
        config.meat_curr = 10
        
        print("mag 1 full")
        print("mag 1 (LED_OFF)")

    def fyllt2(self):
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
            GPIO.output(START_LED_PIN , 0)
            self.ready_togo = False
            #action start 
            print("kör")

        



