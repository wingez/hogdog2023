from gc import callbacks
import imp
import RPi.GPIO as GPIO
from main import builder
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


def placeholder():
    print("test")


def check():


    if mag1_ammo <=2:
        GPIO.output(MAG_1_FILL_LED_PIN, 1)
        print("mag 1 needs refill")
        print("mag 1 low (LED_ON)")


    if mag2_ammo <=1:
        GPIO.output(MAG_2_FILL_LED_PIN, 1)
        print("mag 2 needs refill")
        print("mag 2 low (LED_ON)")

    if heater_on:
        GPIO.output(HEATER_LED_PIN, 1)
        print("heater on (LED)")

    else:
        GPIO.output(HEATER_LED_PIN, 0)
        print("heater off (LED)")

    if #fyll1 behövs
        GPIO.add_event_detect(MAG_1_FILL_PIN, GPIO.RISING, callback=fyllt1 , bouncetime=300)       # fyll 1
        print("mag 1 needs refill")

    if #fyll2 behövs
        GPIO.add_event_detect(MAG_2_FILL_PIN, GPIO.RISING, callback=fyllt2 , bouncetime=300)       # fyll 2
        

    if (mag1_ammo > 0 && runner.meat || mag2_ammo > 0 && !runner.meat) || # !running :
        ready_togo = True
        print("Ready to go")
    

    if ready_togo:
        GPIO.add_event_detect(START_PIN, GPIO.RISING, callback=go , bouncetime=300)   #startknapp


def fyllt1():
    GPIO.output(MAG_1_FILL_LED_PIN , 0)
    mag1_ammo = 10
    
    print("mag 1 full")
    print("mag 1 (LED_OFF)")

def fyllt2():
    GPIO.output(MAG_2_FILL_LED_PIN , 0)
    mag2_ammo = 5
    
    print("mag 2 full")
    print("mag 2 (LED_OFF)")

def start_led_on():
    GPIO.output(START_LED_PIN , 1)

def start_led_off():
    GPIO.output(START_LED_PIN , 0)


def go():
    GPIO.output(START_LED_PIN , 0)
    ready_togo = False
    #action start 
    print("kör")


class Interface:

    #TODO
    GPIO.add_event_detect(MEAT_PIN, GPIO.RISING,   callback=builder.set_meat , bouncetime=300)          #korv
    GPIO.add_event_detect(MEAT_PIN, GPIO.FALLING,  callback=builder.reset_meat , bouncetime=300)

    GPIO.add_event_detect(D1_PIN, GPIO.RISING,   callback=builder.set_d1 , bouncetime=300)           #dressing 1
    GPIO.add_event_detect(D1_PIN, GPIO.FALLING,  callback=builder.reset_d1 , bouncetime=300)

    GPIO.add_event_detect(D2_PIN, GPIO.RISING,   callback=builder.set_d2 , bouncetime=300)          #dressing2    
    GPIO.add_event_detect(D2_PIN, GPIO.FALLING,  callback=builder.reset_d2 , bouncetime=300)
