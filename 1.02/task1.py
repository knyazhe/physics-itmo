import matplotlib.pyplot as plt
import pandas as pd

font = {'size': 16}
plt.rcParams['text.usetex'] = True
plt.rcParams['figure.edgecolor'] = 'black'

data1 = pd.read_csv('data/data_1.csv', delimiter=';')  # 1 task
data2 = pd.read_csv('data/data_2.csv', delimiter=';')  # 2 task
data1.head()

d_x = 0.5 / 100  # m
d_h = 0.05 / 100  # m
d_t = 0.1  # c

y = []
z = []
t1 = data1['t1'].tolist()
t2 = data1['t2'].tolist()

for index, rows in data1.iterrows():
    y.append(float(rows['x2']) - float(rows['x1']))
    z.append((float(rows['t2']) ** 2 - float(rows['t1']) ** 2) / 2)
n = range(len(z))

a = sum(z[i] * y[i] for i in n) / sum((z[i] ** 2) for i in n)  # method of minimal squares (8)
yn = list(map((lambda x: x * a), z))  # method of minimal squares

sko_a = (sum((y[i] - a * z[i]) ** 2 for i in n)
         /
         ((len(z) - 1) * sum(z[i] ** 2 for i in n))) ** 0.5  # (8)

absolute_inac = 2 * sko_a  # абсолютная погрешность (9)
relative_inac = (absolute_inac / a) * 100  # относительная погрешность (10)

print("ускорение a: {}\nСко а: {} \nабсолютная погрешнасть а: {} \nотносительная погрешность: {}%".format(a, sko_a,
                                                                                                          absolute_inac,
                                                                                                          relative_inac))
dy = ((d_x ** 2) * 2) ** 0.5
dz = []
print("y:\n", y, "+-", dy)
print("z:")
for i in range(len(z)):
    dz.append(((-d_t * t1[i]) ** 2 + (d_t * t2[i]) ** 2) ** 0.5)
    print(z[i], "+-", dz[i], end="    ")

# plotting
plt.grid()
plt.ylabel("$x, cm$", font)
plt.xlabel("$t, c$", font)
plt.scatter(z, y, c='red', s=3, zorder=5)
plt.plot(z, yn, color='blue')

plt.savefig("out/task1.png", dpi=500)
plt.savefig("out/task1.eps", dpi=500)
plt.show()
