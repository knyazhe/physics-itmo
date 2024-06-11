import matplotlib.pyplot as plt
import pandas as pd

# task2

font = {'size': 16}
plt.rcParams['text.usetex'] = True
plt.rcParams['figure.edgecolor'] = 'black'


data1 = pd.read_csv('data/data_1.csv', delimiter=';')  # 1 task
data2 = pd.read_csv('data/data_2.csv', delimiter=';')  # 2 task
data1.head()

d_x = 0.5 / 100  # m
d_h = 0.05 / 100  # m
d_t = 0.1  # c

N = 5
sina = [0.] * N
t1_mean = [0.000] * N
t2_mean = [0.000] * N

for i in range(N):
    # (11)
    vari = ((-data2.iloc[i * 5]['h'] + data1.iloc[0]['h0']) - (-data2.iloc[i * 5]['h`'] + data1.iloc[0]['h0`']))
    vari2 = (data2.iloc[i * 5]['x`']) - (data2.iloc[i * 5]['x'])
    sina[i] = (vari / vari2)
for i in range(25):
    t1_mean[int(i/5)] += float(data2.iloc[i]['t1'])
    t2_mean[int(i/5)] += float(data2.iloc[i]['t2'])
for i in range(N):
    t1_mean[i] = t1_mean[i]/N
    t2_mean[i] = t2_mean[i]/N
print("sina:")
for i in range(N):
    print(sina[i], end="  ")
print("\nt1 среднее:")
for i in t1_mean:
    print("{} +- {}".format(i, d_t), end="   ")
print("\nt2 среднее:")
for i in t2_mean:
    print("{} +- {}".format(i, d_t), end="   ")
print()

a = [0.] * N  # a - ускорение
da = [0.] * N  # погрешность a

for i in range(N):
    a[i] = 2 * (data2.iloc[i * 5]['x2'] - data2.iloc[i * 5]['x1']) / ((t2_mean[i] ** 2) - (t1_mean[i] ** 2))  # 12

    da[i] = a[i] * ((2 * (d_x ** 2) / ((data2.iloc[i * 5]['x2'] - data2.iloc[i * 5]['x1']) ** 2))
                    +
                    4 * ((t1_mean[i] * d_t) ** 2 + (t2_mean[i] * d_t) ** 2) /
                    ((t2_mean[i]) ** 2 - (t1_mean[i]) ** 2) ** 2) ** 0.5  # (13)
print("а среднее с погрешностями: ")
for i in range(N):
    print("{} +- {}".format(a[i], da[i]), end="   ")

a_sina_sum = 0
sina2_sum = 0
for i in range(N):
    a_sina_sum += (a[i] * sina[i])
    sina2_sum += sina[i] ** 2
B = (a_sina_sum - (1 / N) * sum(a) * sum(sina)) / (sina2_sum - (1 / N) * ((sum(sina)) ** 2))  # (14)
A = (1 / N) * (sum(a) - B * sum(sina))  # (15)
print("\nB = g = {}\nA = {}".format(B, A))

d = 0
d2 = 0
D = sina2_sum - (1 / N) * (sum(sina) ** 2)  # (18)
for i in range(N):
    tmp = (a[i] - (A + B * sina[i]))
    d += tmp  # (17)
    d2 += tmp ** 2
og = (d2 / (D * (N - 2))) ** 0.5  # (16)
dg = 2 * og  # (19)
eg = dg / B * 100  # (20)

print("СКО g: {} \n абсолют погреш g: {} \n относительная погреш g: {}%".format(og, dg, eg))

# g в санкт птеребурге abs(B-g_spb) сравнить dg 7 пункт
g_spb = 9.8195
print("абсолютное отклонение эксп от спб табличного: {} ".format(abs(B-g_spb)))

yn = list(map((lambda x: A + B * x), sina))  # method of minimal squares

plt.grid()
plt.ylabel("$a$", font)
plt.xlabel(r"$\sin{\alpha}$", font)
plt.scatter(sina, a, c='red', s=3, zorder=5)
plt.plot(sina, yn, color='blue')
plt.savefig("out/task2.png", dpi=500)
plt.show()
