import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

np.random.seed(42)

X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

model = LinearRegression()
model.fit(X, y)

X_new = np.array([[0], [2]])
y_pred = model.predict(X_new)

plt.scatter(X, y, label='Original data')
plt.plot(X_new, y_pred, 'r-', label='Linear regression line')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()

plt.show()