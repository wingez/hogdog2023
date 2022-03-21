from gc import callbacks
import imp
import RPi.GPIO as GPIO
from main import builder
#GPIO.setmode(GPIO.BOARD)

MEAT_PIN=XX
D1_PIN=XX
D2_PIN=XX
START_PIN=XX
START_LED_PIN=XX
MAG_1_FILL_PIN=XX
MAG_2_FILL_PIN=XX
MAG_1_FILL_LED_PIN=XX
MAG_2_FILL_LED_PIN=XX
HEATER_LED_PIN=XX


def placeholder():
    print("test")


def check():
    if #mag 1 low
        GPIO.output(MAG_1_FILL_LED_PIN, 1)


    if #mag 2 low
        GPIO.output(MAG_2_FILL_LED_PIN, 1)

    if #heater på
        GPIO.output(HEATER_LED_PIN, 1)

    else:
        GPIO.output(HEATER_LED_PIN, 0)

    if #fyll1 behövs
        GPIO.add_event_detect(MAG_1_FILL_PIN, GPIO.RISING, callback=fyllt1 , bouncetime=300)       # fyll 1
    
    if #fyll2 behövs
        GPIO.add_event_detect(MAG_2_FILL_PIN, GPIO.RISING, callback=fyllt2 , bouncetime=300)       # fyll 2

    if #redo
        GPIO.add_event_detect(START_PIN, GPIO.RISING, callback=go , bouncetime=300)   #startknapp


def fyllt1():
    GPIO.output(MAG_1_FILL_LED_PIN,0)
    #nollställ behov
    print("mag 1 fullt")

def fyllt2():
    GPIO.output(MAG_2_FILL_LED_PIN,0)
    #nollställ behov
    print("mag 2 fullt")

def start_led_on():
    GPIO.output(HEATER_LED_PIN,1)

def start_led_off():
    GPIO.output(HEATER_LED_PIN,0)


def go():
    GPIO.output(HEATER_LED_PIN,0)
    #action
    print("kör")


class Interface:

    #TODO
    GPIO.add_event_detect(MEAT_PIN, GPIO.RISING, callback=builder.set_meat , bouncetime=300)          #korv
    GPIO.add_event_detect(MEAT_PIN, GPIO.FALLING,  callback=builder.reset_meat , bouncetime=300)

    GPIO.add_event_detect(D1_PIN, GPIO.RISING,  callback=builder.set_d1 , bouncetime=300)           #dressing 1
    GPIO.add_event_detect(D1_PIN, GPIO.FALLING,  callback=builder.reset_d1 , bouncetime=300)

    GPIO.add_event_detect(D2_PIN, GPIO.RISING,  callback=builder.set_d2 , bouncetime=300)          #dressing2    
    GPIO.add_event_detect(D2_PIN, GPIO.FALLING,  callback=builder.reset_d2 , bouncetime=300)
