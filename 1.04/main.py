import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import myphlib as ph

font = {'size': 16}
plt.rcParams['text.usetex'] = True
plt.rcParams['figure.edgecolor'] = 'black'

k_student = 2.8  # student's coefficient

N = 6  # number of measuring
h = 0.7  # meters
d_stup = 0.046  # meters
g_spb = 9.8195
secund_inac = 0.005
l1 = 0.057
l0 = 0.025
b = 0.04


task = pd.read_csv('data/data4.csv', delimiter=';')
out_tables = [pd.DataFrame() for _ in range(11)]

out_tables[0]['t_mean'] = pd.concat([task['t1'], task['t2'], task['t3']], axis=1).mean(axis=1)
out_tables[0]['t_inac'] = ((ph.measure_sko(out_tables[0]['t_mean']) * 4.3) ** 2 + (2 * secund_inac / 3) ** 2) ** 0.5

out_tables[0]['a'] = 2 * h / (out_tables[0]['t_mean'] ** 2)
out_tables[0]['eps'] = 2 * out_tables[0]['a'] / d_stup
out_tables[0]['M'] = (task['m'] * d_stup / 2) * (g_spb - out_tables[0]['a'])

out_tables[0]['a_inac'] = ((4 * h / (out_tables[0]['t_mean'] ** 3) * out_tables[0]['t_inac']) ** 2) ** 0.5  # a inac
out_tables[0]['eps_inac'] = (((8 * h * out_tables[0]['t_inac']) / (out_tables[0]['t_mean']**3 * d_stup)) ** 2) ** 0.5  # eps inaccuracy
out_tables[0]['M_inac'] = (((2 * task['m'] * d_stup * out_tables[0]['t_inac']) / (out_tables[0]['t_mean'] ** 3)) ** 2) ** 0.5  # M inac

plt.grid()
plt.title(r"$M(\varepsilon)$", font)
plt.ylabel(r"$M$, $N \cdot m$", font)
plt.xlabel(r"$\varepsilon$, $rad/s^2$", font)
colors = ['red', 'orange', 'green', 'blue', 'pink', 'purple']

for i in range(N):
    x = out_tables[0]['eps'][i * 4:(i + 1) * 4]
    y = out_tables[0]['M'][i * 4:(i + 1) * 4]

    plt.scatter(x, y, c=colors[i], s=3, zorder=5, label='$riska$ $' + str(i + 1) + '$')
    mnk_i = ph.MNK(x, y)
    I, tr = mnk_i.a, mnk_i.b
    out_tables[1].at[i, 'I'] = I
    out_tables[1].at[i, 'tr'] = tr
    plt.plot(x, x * I + tr, color='darkgray')

plt.errorbar(out_tables[0].at[0, 'eps'], out_tables[0].at[0, 'M'], out_tables[0].at[0, 'eps_inac'],
             out_tables[0].at[0, 'M_inac'])
out_tables[1]['R'] = [l1 + (n - 1) * l0 + b / 2 for n in range(1, N + 1)]
out_tables[1]['R2'] = out_tables[1]['R'] ** 2

ph.save("task1", plt)

plt.grid()
plt.title(r"$I(R^2)$", font)
plt.xlabel("$R^2$, $m^2$", font)
plt.ylabel("$I$, $kg \cdot m^2$", font)

plt.scatter(out_tables[1]['R2'], out_tables[1]['I'], c='blue', s=3, zorder=5)
mnk1 = ph.MNK(out_tables[1]['R2'], out_tables[1]['I'])
m_ut = mnk1.a / 4
I_0 = mnk1.b
out_tables[1]['m_ut'] = m_ut
out_tables[1]['I_0'] = I_0
out_tables[1]['m_ut_inac'] = mnk1.a_inac
out_tables[1]['I_0_inac'] = mnk1.b_inac
plt.plot(out_tables[1]['R2'], out_tables[1]['R2'] * 4 * m_ut + I_0, c='red')

ph.save("task2", plt)
ph.save_tables("task", out_tables, [0, 1])