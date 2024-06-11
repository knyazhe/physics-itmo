import math

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import myphlib as ph

font = {'size': 16}
plt.rcParams['text.usetex'] = True
plt.rcParams['figure.edgecolor'] = 'black'

g_spb = 9.8195
k_student = 0  # student's coefficient

tables_indexes = [2, 3, 4]
tables = [pd.DataFrame() for _ in range(max(tables_indexes) + 1)]
for i in [2, 3, 4]:
    tables[i] = pd.read_csv(f'data/table{i}.csv', sep=';', decimal='.')

# (1)
n = 10
tables[2]['t'] = (tables[2]['t1'] + tables[2]['t2'] + tables[2]['t3']) / 3
# tables[2]['T'] = (tables[2]['t']) / n
T_start = tables[2]['t'][5]/10

tables[3]['t'] = (tables[3]['t1'] + tables[3]['t2'] + tables[3]['t3']) / 3
tables[3]['T'] = (tables[3]['t']) / n
# (2)
plt.grid()
plt.title(r"$A(t)$", font)
plt.ylabel(r"$A$, $degrees$", font)
plt.xlabel(r"$t$, $sec$", font)
plt.ylim(0, 26)
plt.plot(tables[2]['t'][:-1], tables[2]['gr'][:-1])
ph.save("lab5.1", plt)
print("Сухой тип трения")

mnk1 = ph.MNK(tables[2]['t'][:-1], tables[2]['gr'][:-1])
A0 = mnk1.b
k = mnk1.a
print(A0, k)
d_phi_k = k * T_start / (-4)
n_k = (A0/(4*d_phi_k.max()))

print(f"d_phi (ширина зоны застоя) {d_phi_k.mean()}, колебания прекратятся через {n_k} колебаний, T: {T_start}")
# (3)
l0 = 0.025  #meters
d_l0 = 0.002
l1 = 0.057
d_l1 = 0.005
b = 0.040
d_b = 0.005
m_gr = 0.408
d_m_gr = 0.0005
I0 = 0.008  # n*m
m_sys = m_gr * 4

tables[4]['R_down'] = l1 + (6 - 1) * l0 + b / 2
tables[4]['R_up'] = l1 + (1 - 1) * l0 + b / 2
tables[4]['R_bok'] = l1 + (pd.Series(range(1, 7)) - 1) * l0 + b / 2
# (4)
tables[4]['I_gr'] = m_gr * (tables[4]['R_up'] ** 2 + 2 * tables[4]['R_bok'] ** 2 + tables[4]['R_down'] ** 2)
tables[4]['I'] = tables[4]['I_gr'] + I0
# (5)
plt.grid()
plt.title(r"$T^2(I)$", font)
plt.ylabel("$T^2$, $sec^{-2}$", font)
plt.xlabel("$I$, $kg \cdot m^2$", font)
plt.plot(tables[4]['I'], tables[3]['T'] ** 2)
ph.save("lab5.2", plt)

mnk1 = ph.MNK(tables[4]['I'], tables[3]['T'] ** 2)
ml = 1 / mnk1.a * 4 * math.pi / g_spb
# (6)
v_up = []
v_down  = []
v_left  = []
v_right = []
for i in range(6):
    v_up.append(np.array((0, tables[4]['R_up'][i])))
    v_down.append(np.array((0, -tables[4]['R_down'][i])))
    v_left.append(np.array((-tables[4]['R_bok'][i], 0)))
    v_right.append(np.array((tables[4]['R_bok'][i], 0)))

v_up = pd.Series(v_up)
v_down = pd.Series(v_down)
v_left = pd.Series(v_left)
v_right = pd.Series(v_right)

# print(v_up, v_down, v_left, v_right)
tables[4]['l_teor'] = ((v_down + v_up + v_left + v_right)/4)
for i in range(6):
    x =tables[4]['l_teor'][i]
    tables[4]['l_teor'][i] = float(-x[1])

print("\n", tables[4]['l_teor'], "\n")
# (7)
tables[4]['l_pr_e'] = (tables[3]['T'] ** 2 * g_spb) / (4 * math.pi**2)
# (8)
tables[4]['l_pr_t'] = I0/(m_sys * tables[4]['l_teor'])+tables[4]['l_teor']

ph.save_tables("out_tables_new", tables, [2, 3, 4])
