import numpy as np
import math
import matplotlib.pyplot as plt


def servo_smoothed(start, end, step):
  #LINSPACE MUST BE FROM -1.5 to 1.5 due to rounding problems (Higher eg. -2,2 is fine aswell)
  y_values_int = [ round((end-start)*sigmoid(x)+start) for x in np.linspace(-1.5, 1.5, step)]
  return y_values_int


def sigmoid(x, k=3):
    return (1 / (1 + np.exp(-k *x)))


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
