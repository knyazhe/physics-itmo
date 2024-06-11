import matplotlib.pyplot as plt
import pandas as pd

font = {'size': 16}
plt.rcParams['text.usetex'] = True
plt.rcParams['figure.edgecolor'] = 'black'

t_stu = 2.8  # student's coefficient
N = 7  # number of measuring
g_spb = 9.82  # g in spb

task2 = [pd.read_csv(f'data/task2/data3.2.{i}.csv', delimiter=';') for i in [5, 6]]
task2 = dict(zip([5, 6], task2))
out_tables = [pd.DataFrame() for _ in range(2)]
out_tables = dict(zip([11, 12], out_tables))

plt.grid()
plt.ylabel("$T$", font)
plt.xlabel(r"$a$", font)
colors = [('red', 'blue'), ('orange', 'green')]

for i, j in [(5, 11), (6, 12)]:
    out_tables[j]['a'] = (task2[i]['v2'] ** 2 - task2[i]['v1'] ** 2) / (2 * (task2[i]['x2'] - task2[i]['x1']))  # 25
    out_tables[j]['T'] = (task2[i]['m']) * (g_spb - out_tables[j]['a'])  # 25

    # тут типа мнк, было неприятно
    # out_tables[j]['sina'] = (M1 - task2[i]['m1']) / (task2[i]['m1'] * g_spb)
    # out_tables[j]['T'] = task2[i]['m'] * (g_spb - out_tables[j]['a']) + task2[i]['m1'] * g_spb * out_tables[j]['sina']  # 25

    M1 = (sum((out_tables[j]['a'] - out_tables[j]['a'].mean()) * (out_tables[j]['T'] - out_tables[j]['T'].mean()))
          /
          sum((out_tables[j]['a'] - out_tables[j]['a'].mean()) ** 2))

    F_TR = out_tables[j]['T'].mean() - M1 * out_tables[j]['a'].mean()
    yn = list(map((lambda x: F_TR + M1 * x), out_tables[j]['a']))

    out_tables[j]['d'] = (out_tables[j]['T'] - (F_TR + M1 * out_tables[j]['a']))
    D = sum((out_tables[j]['a'] - out_tables[j]['a'].mean()) ** 2)
    sko_M1 = sum(out_tables[j]['d'] ** 2) / (D * (N - 2))
    sko_F_TR = sum(out_tables[j]['d'] ** 2) / (N - 2) * (1 / N + (out_tables[j]['a'].mean() ** 2) / D)
    out_tables[j]['d_M1'] = ((2 * sko_F_TR) ** 2 + (2 * sko_M1 * out_tables[j]['a'].max()) ** 2) ** 0.5
    out_tables[j]['M1'] = M1
    out_tables[j]['F_TR'] = F_TR
    out_tables[j]['sko_M1'] = sko_M1
    out_tables[j]['sko_F_TR'] = sko_F_TR

    plot_color = colors[i - 5][0]
    scat_color = colors[i - 5][1]
    plt.scatter(out_tables[j]['a'], out_tables[j]['T'], c=scat_color, s=3, zorder=5)
    plt.plot(out_tables[j]['a'], yn, color=plot_color, label=f"$Table$ ${i}$")

plt.legend()
plt.savefig("out/task2.png", dpi=500)
plt.show()

with pd.ExcelWriter('out/task2.xlsx') as writer:
    for i in [11, 12]:
        table = pd.DataFrame(out_tables[i])
        table.to_excel(writer, sheet_name=f"Table{i}", index=False)
