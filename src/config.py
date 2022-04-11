import RPi.GPIO as GPIO

pins = {
    'interface': {
        'meat': 7,
        'd1': 6,
        'd2': 13,
        's_led': 21,
        's_btn': 20,
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

meat_curr = 0;
veg_curr = 0;

degStates = {}

degStates["heater"]     = 170
degStates["d_final"]    = 5
degStates["d_takeoff"]  = 15
degStates["b_final"]    = 155
degStates["b_takeoff"]  = 165
degStates["d1"]         = 120
degStates["d2"]         = 90

meat_degs = [120,115,110,105,100,95,90,85,85,80];
veg_degs = [75,70,65,60,55];
degStates["mags"] = 75

for i, deg in enumerate(meat_degs):
    degStates[f"meat{i}"] = deg;

for i, deg in enumerate(veg_degs):
    degStates[f"veg{i}"] = deg;