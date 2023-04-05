import numpy as np
import matplotlib.pyplot as plt

def interpolate_2(xy_values, output_length, resolution):
    x_values, y_values = zip(*xy_values)
    x_min, x_max = min(x_values), max(x_values)
    num_points = output_length * resolution

    #Generate x
    interp_x_values = np.linspace(x_min, x_max, num_points)
    #Interpolate y for each interp_x_value
    interp_y_values = np.interp(interp_x_values, x_values, y_values)

    #zip em' back
    interp_xy_values = list(zip(interp_x_values, interp_y_values))

    #sample interpolated values to the output length
    sampled_xy_values = [interp_xy_values[i] for i in range(0, len(interp_xy_values), resolution)]

    return sampled_xy_values


def interpolate(input_vector, output_length, resolution):
    # Create an array of output values
    output_array = np.zeros((output_length,))
    print(len(input_vector))
    print(output_length)
    # Calculate the step size for linear interpolation
    #step = len(input_vector) / (output_length)
    step = ((len(input_vector) - 1)/float(output_length - 1) )
    # Fill in the output array with linearly interpolated values
    for i in range(output_length):
        index = i * step
        lower_index = int(index)
        upper_index = min(lower_index + 1, len(input_vector) - 1)
        fraction = index - lower_index
        output_array[i] = input_vector[lower_index] * (1 - fraction) + input_vector[upper_index] * fraction

    # Interpolate the output array to match the desired resolution
    resampled_array = np.zeros((int(output_length * resolution),))
    for i in range(int(output_length * resolution)):
        index = i / resolution
        lower_index = int(index)
        upper_index = min(lower_index + 1, len(output_array) - 1)
        fraction = index - lower_index
        resampled_array[i] = output_array[lower_index] * (1 - fraction) + output_array[upper_index] * fraction

    return resampled_array


input_vector = np.array([0,40,60,80,100])
output_length = 100
resolution = 0.1

# Call the interpolate function to get the lookup array
lookup_array = interpolate(input_vector, output_length, resolution)

print(len(lookup_array))
# Plot the lookup array using matplotlib
plt.plot(lookup_array)
plt.title('Linearly interpolated lookup array')
plt.xlabel('Index')
plt.ylabel('Value')



#This is not as structured because of little time
input_data = [(1, 1), (2, 8), (3, 27), (4, 64), (5, 125)]

# Define the output length and resolution
output_length = 100
resolution = 1

# Generate the interpolated data
interpolated_data = interpolate_2(input_data, output_length, resolution)

print(len(interpolated_data))
# Separate the x and y values into two arrays

# Plot the input and interpolated data
plt.plot(*zip(*interpolated_data), 'o', label='Interpolated Data')
plt.plot(*zip(*input_data), 'o', label='Input Data')



x_val, y_val = zip(*input_data)
# Look up the y value for a given x value
x = 1.5
y = np.interp(x, x_val, y_val)
print(f"The interpolated y value for x={x} is {y}")

plt.legend()
plt.show()



