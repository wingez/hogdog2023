import numpy as np

def servo_smoothed(start, end, step):
  #LINSPACE MUST BE FROM -1.5 to 1.5 due to rounding problems (Higher eg. -2,2 is fine aswell)
  y_values_int = [ round((end-start)*sigmoid(x)+start) for x in np.linspace(-1.5, 1.5, step)]
  return y_values_int


def sigmoid(x, k=3):
    return (1 / (1 + np.exp(-k *x)))


if __name__ == '__main__':
  start = 50
  end = 160
  steps = 100
  y_servo = servo_smoothed(50, 160, steps)
  #print(y_servo)

