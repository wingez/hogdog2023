import RPi.GPIO as GPIO

meat_curr = 0;
veg_curr = 0;

degStates = {}

degStates["heater"]     = 0
degStates["d_final"]    = 160
degStates["b_final"]    = 0
degStates["d1"]         = 30
degStates["d2"]         = 50

meat_degs = [35,40,45,50,55,60,65,70,75,80];
veg_degs = [85,90,95,100,105];

for i, deg in enumerate(meat_degs):
    degStates[f"meat{i}"] = deg;

for i, deg in enumerate(veg_degs):
    degStates[f"veg{i}"] = deg;