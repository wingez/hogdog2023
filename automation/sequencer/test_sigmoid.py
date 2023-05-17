import numpy as np
import math
import matplotlib.pyplot as plt
from sigmoid_gen import servo_smoothed, sigmoid

if __name__ == '__main__':
  steps = 100
  xy_values = [(x, sigmoid(x)) for x in np.linspace(0, 1, steps)]
  x_values = [xy[0] for xy in xy_values]
  y_servo_int = servo_smoothed(30, 70, steps)
  print(y_servo_int)


  # Prints the x and y values in the format (x, y)
  # Create a new figure and axis object
  fig, ax = plt.subplots()

  plt.xlabel("time")
  plt.ylabel("angle")
  # Plot the (x, y) values as a scatter plot
  ax.scatter(x_values, y_servo_int)


  # Show the plot
  plt.show()
