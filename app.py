# Constants
c = 3.0e8
e = 1.602e-19
actual_value = 6.626e-34

wavelengths = []
frequencies = []
voltages = []

print("Enter 5 data points of wavelength and voltage:")
for i in range(1, 6):
    w = float(input(f"Enter {i} wavelength in nm: "))
    v = float(input(f"Enter {i} voltage: "))

    freq = c / (w * 1e-9)

    wavelengths.append(w)
    frequencies.append(freq)
    voltages.append(v)

# Find the lowest wavelength (highest freq) and highest wavelength (lowest freq)
min_idx = wavelengths.index(min(wavelengths))
max_idx = wavelengths.index(max(wavelengths))

# Calculate slope using end-to-end points (matches hand-drawn endpoints)
change_in_y = voltages[min_idx] - voltages[max_idx]
change_in_x = frequencies[min_idx] - frequencies[max_idx]

slope = change_in_y / change_in_x
Experimental_h = slope * e

print("\n----------------------------------")
print("Value of slope             :", slope)
print("Value of experimental h is :", Experimental_h, "J·s")
print("Actual value of h is        :", actual_value, "J·s")

percentage_error = (abs(Experimental_h - actual_value) / actual_value) * 100
print("Percentage Error            :", round(percentage_error, 2), "%")
print("----------------------------------")
