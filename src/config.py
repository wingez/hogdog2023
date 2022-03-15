import RPi.GPIO as GPIO

meat_curr = 0;
veg_curr = 0;

degStates = {}

degStates["heater"]     = 170
degStates["d_final"]    = 0
degStates["d_takeoff"]  = 10
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