import lab2_oppgave1 as data
import numpy as np 
import matplotlib.pyplot as plt

#Plot quality level over time
x_axis = np.array([i for i in range(24)])
y_axis = np.array([item for item in data.mos_per_hour])

plt.plot(x_axis, y_axis)

plt.xlabel("hours")
plt.ylabel("MOS score")

plt.show()
