import matplotlib.pyplot as plt

x = [0,1,2,3,4]
y = [0,2,4,6,8]

# Add a title (specify font parameters with fontdict)
plt.title('Our First Graph!', fontdict={'fontname': 'Comic Sans MS', 'fontsize': 20})
plt.plot(x, y)
plt.title("Basic Line Graph")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()