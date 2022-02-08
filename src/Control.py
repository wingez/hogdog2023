import Serial

class Control:

    def servo(serv, deg, speed, time):
        msg = f"[{serv}]<{deg},{time}>"
        Serial.write(msg)


        # "[d_arm]<39,10,30>|"
