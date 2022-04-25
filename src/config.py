import RPi.GPIO as GPIO

pins = {
    'interface': {
        'meat': 7,
        'd1': 6,
        'd2': 13,
        's_led': 20,
        's_btn': 21,
        'mag2_led': 16,
        'mag2_btn': 12,
        'mag1_led': 26,
        'mag1_btn': 5,
        'heater_led': 19
    },
    'arm': {
        'down': 22,
        'up': 27
    }
}

meat_curr = 9;      # MAX 9
veg_curr = 4;       # MAX 4

degStates = {}

degStates["heater"]     = 180
degStates["d_final"]    = 5
degStates["d_takeoff"]  = 16
degStates["b_final"]    = 155
degStates["b_takeoff"]  = 165
degStates["d1"]         = 120
degStates["d2"]         = 90
degStates["mags"]       = 71

veg_start = 43;
veg_end = 71;

meat_start = 80
meat_end = 143

for i in range(0, 10):
    deg = i*abs(meat_end - meat_start)/9 + meat_start
    degStates[f"meat{i}"] = deg;

for i in range(0, 5):
    deg = i*abs(veg_end - veg_start)/4 + veg_start
    degStates[f"veg{i}"] = deg;