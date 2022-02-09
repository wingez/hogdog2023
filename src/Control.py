import time

class Control:

    def cservo(sch, cw, timeout, stop):

        timeout = time.time() + timeout

        if cw:
            while time.time() > timeout:
                if stop:
                    break
                #TODO kör servo sch clockwise
        else:
            while time.time() > timeout:
                if stop:
                    break
                #TODO kör servo sch ccw

    def rservo(sch, pos):
        #TODO kör servo sch till deg
        return None


degStates = {}

degStates["heater"]     = 0
degStates["d_mag"]      = 0
degStates["d_final"]    = 0
degStates["b_mag"]      = 0
degStates["b_final"]    = 0
degStates["d1"]         = 0
degStates["d2"]         = 0