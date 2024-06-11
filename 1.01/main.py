import matplotlib.pyplot as plt
import numpy as np
import math

m_data = [7.91, 7.91, 7.84, 8.19, 8, 7.9, 8.28, 7.98, 8.29, 7.88, 8.18, 7.93, 7.91, 7.96, 8, 7.95, 7.91, 7.98, 8.1,
          7.91, 8.14, 8.03, 8.19, 8, 8.18, 8.28, 7.76, 8.23, 7.7, 8.31, 7.92, 7.99, 7.95, 8, 7.93, 7.87, 8.24, 8.11,
          8.21, 8.23, 7.98, 8.03, 8.21, 7.77, 8.04, 8.26, 8.09, 7.81, 8.03, 8.03]
N = len(m_data)  # number of measuring

t_mean = sum(m_data) / N  # arithmetic mean

tmp = 0
for i in range(N):
    tmp += (m_data[i] - t_mean) ** 2
sd = (tmp / (N - 1)) ** (1 / 2)  # standard deviation


def ro(t):
    out = (1 / ((2 * math.pi) ** (1 / 2) * sd)) * math.exp(-(t - t_mean) ** 2 / (2 * (sd ** 2)))
    return out


font = {'font': 'dejavu',
        'family': 'serif',
        'weight': 'normal',
        'size': 16,
        }
plt.rcParams["mathtext.fontset"] = 'dejavuserif'
# gauss
x = np.linspace(min(m_data), max(m_data), 1000)  # X от -5 до 5
y = list(map(ro, x))
plt.plot(x, y, color='red')

# matplotlib histogram
plt.hist(m_data, color='lightblue', edgecolor='black', bins=7, density=True)
# Add labels
plt.title('Histogram', fontdict=font)
plt.xlabel('t, с', fontdict=font)
plt.ylabel('$\\frac{\\Delta N}{N\\Delta t}$', fontdict=font)
# plt.savefig('output.eps')
plt.show()
