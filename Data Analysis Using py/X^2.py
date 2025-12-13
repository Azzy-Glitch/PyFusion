import numpy as np
import matplotlib.pyplot as plt

# Generate data
x = np.linspace(0, 10, 100)
y = x ** 2     

# Plot
plt.plot(x, y)
plt.title("Simple Graph: y = x^2")
plt.xlabel("x values")
plt.ylabel("y values")
plt.grid(True)

# Show the graph
plt.show()
