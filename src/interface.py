from gc import callbacks
import imp
import RPi.GPIO as GPIO
from main import builder1
from main import runner1
#GPIO.setmode(GPIO.BOARD)

MEAT_PIN=17
D1_PIN=27
D2_PIN=22
START_PIN=23
START_LED_PIN=24
MAG_1_FILL_PIN=10
MAG_2_FILL_PIN=9
MAG_1_FILL_LED_PIN=11
MAG_2_FILL_LED_PIN=25
HEATER_LED_PIN=8



class Interface: 

    def __init__(self):
        self.mag1_ammo=10
        self.mag2_ammo=5
        self.ready_togo=True


        GPIO.add_event_detect(MEAT_PIN, GPIO.RISING,   callback=builder1.set_meat , bouncetime=300)          #korv
        GPIO.add_event_detect(MEAT_PIN, GPIO.FALLING,  callback=builder1.reset_meat , bouncetime=300)

        GPIO.add_event_detect(D1_PIN, GPIO.RISING,   callback=builder1.set_d1 , bouncetime=300)           #dressing 1
        GPIO.add_event_detect(D1_PIN, GPIO.FALLING,  callback=builder1.reset_d1 , bouncetime=300)

        GPIO.add_event_detect(D2_PIN, GPIO.RISING,   callback=builder1.set_d2 , bouncetime=300)          #dressing2    
        GPIO.add_event_detect(D2_PIN, GPIO.FALLING,  callback=builder1.reset_d2 , bouncetime=300)

        GPIO.add_event_detect(START_PIN, GPIO.RISING, callback=self.go , bouncetime=300)   #startknapp

        GPIO.add_event_detect(MAG_1_FILL_PIN, GPIO.RISING, callback=self.fyllt1 , bouncetime=300)       # fyll 1

        GPIO.add_event_detect(MAG_2_FILL_PIN, GPIO.RISING, callback=self.fyllt2 , bouncetime=300)       # fyll 2
      

    def placeholder():
        print("test")


    def mag1_decrease(self):
        self.mag1_ammo-=1


    def mag2_decrease(self):
        self.mag2_ammo-=1
        

    def check(self):

        if self.mag1_ammo <=2:
            GPIO.output(MAG_1_FILL_LED_PIN, 1)
            print("mag 1 needs refill")
            print("mag 1 low (LED_ON)")


        if self.mag2_ammo <=1:
            GPIO.output(MAG_2_FILL_LED_PIN, 1)
            print("mag 2 needs refill")
            print("mag 2 low (LED_ON)")

        #if #heater_on:
         #  GPIO.output(HEATER_LED_PIN, 1)
         #  print("heater on (LED)")

        else:
            GPIO.output(HEATER_LED_PIN, 0)
            print("heater off (LED)")
            
            

        if ((self.mag1_ammo > 0 and builder1.meat) or (self.mag2_ammo > 0 and not builder1.meat)):# and not running :
            self.ready_togo = True
            self.start_led_on()
            print("Ready to go")
        


    def fyllt1(self):
        GPIO.output(MAG_1_FILL_LED_PIN , 0)
        self.mag1_ammo = 10
        
        print("mag 1 full")
        print("mag 1 (LED_OFF)")

    def fyllt2(self):
        GPIO.output(MAG_2_FILL_LED_PIN , 0)
        self.mag2_ammo = 5
        
        print("mag 2 full")
        print("mag 2 (LED_OFF)")

    def start_led_on():
        GPIO.output(START_LED_PIN , 1)

    def start_led_off():
        GPIO.output(START_LED_PIN , 0)


    def go(self):
        if self.ready_togo:
            self.start_led_off()
            GPIO.output(START_LED_PIN , 0)
            self.ready_togo = False
            #action start 
            print("kör")

        



