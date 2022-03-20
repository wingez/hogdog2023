
class Interface:
    #TODO
    GPIO.add_event_detect(XX, GPIO.RISING, set_meat , bouncetime=300)
    GPIO.add_event_detect(XX, GPIO.FALLING, reset_meat , bouncetime=300)

    GPIO.add_event_detect(XX, GPIO.RISING, set_d1 , bouncetime=300)
    GPIO.add_event_detect(XX, GPIO.FALLING, reset_d1 , bouncetime=300)

    GPIO.add_event_detect(XX, GPIO.RISING, set_d2 , bouncetime=300)
    GPIO.add_event_detect(XX, GPIO.FALLING, reset_d2 , bouncetime=300)

    GPIO.add_event_detect(XX, GPIO.RISING,  , bouncetime=300)   
    GPIO.add_event_detect(XX, GPIO.FALLING,  , bouncetime=300)

    GPIO.add_event_detect(XX, GPIO.RISING,  , bouncetime=300)
    GPIO.add_event_detect(XX, GPIO.FALLING,  , bouncetime=300)


    def placeholder():
        print("test")