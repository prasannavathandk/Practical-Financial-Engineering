import numpy as np

val1 = np.load("val1.npy")
val2 = np.load("val2.npy")
print(val1, val2)
print(np.subtract(val1, val2))