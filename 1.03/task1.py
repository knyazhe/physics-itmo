import matplotlib.pyplot as plt
import pandas as pd

font = {'size': 16}
plt.rcParams['text.usetex'] = True
plt.rcParams['figure.edgecolor'] = 'black'

t_stu = 2.8  # student's coefficient
N = 5  # number of measuring

task1 = [pd.DataFrame() for i in range(5)]
task1[1:5] = [pd.read_csv(f'data/task1/data3.1.{i}.csv', delimiter=';') for i in [1, 2, 3, 4]]
out_tables = [pd.DataFrame() for i in range(11)]

for i, j in [(7, 1), (8, 2)]:
    out_tables[i]['p10x'] = task1[j]['m1'] * task1[j]['v10']  # (15)
    out_tables[i]['p1x'] = task1[j]['m1'] * task1[j]['v1']  # (15)
    out_tables[i]['p2x'] = task1[j]['m2'] * task1[j]['v2']  # (15)
    out_tables[i]['dp'] = (out_tables[i]['p1x'] + out_tables[i]['p2x']) / out_tables[i]['p10x'] - 1  # (16)
    out_tables[i]['dw'] = (task1[j]['m1'] * (task1[j]['v1'] ** 2) + task1[j]['m2'] * (
            task1[j]['v2'] ** 2)) / (task1[j]['m1'] * (task1[j]['v10'] ** 2)) - 1  # (17)
    dp_mean = sum(out_tables[i]['dp']) / N  # (18)
    dw_mean = sum(out_tables[i]['dw']) / N  # (18)
    out_tables[i]['dp_inac'] = t_stu * (
            sum((out_tables[i]['dp'] - dp_mean) ** 2) / (N * (N - 1))) ** 0.5  # (19)
    out_tables[i]['dw_inac'] = t_stu * (
            sum((out_tables[i]['dw'] - dw_mean) ** 2) / (N * (N - 1))) ** 0.5  # (19)

for i, j in [(9, 3), (10, 4)]:
    print(i, j)
    out_tables[i]['p10'] = task1[j]['m1'] * task1[j]['v10']  # (20)
    out_tables[i]['p'] = (task1[j]['m1'] + task1[j]['m2']) * task1[j]['v']  # (21)
    out_tables[i]['dp'] = out_tables[i]['p'] / out_tables[i]['p10'] - 1  # (22)
    out_tables[i]['dwe'] = (((task1[j]['m1'] + task1[j]['m2']) * (task1[j]['v'] ** 2)) / (
            task1[j]['m1'] * (task1[j]['v10'] ** 2))) - 1  # (23)
    out_tables[i]['dwt'] = -((task1[j]['m2']) / (task1[j]['m1'] + task1[j]['m2']))  # (24)
    dp_mean = sum(out_tables[i]['dp']) / N
    dw_mean = sum(out_tables[i]['dwe']) / N
    out_tables[i]['dp_inac'] = t_stu * (
            sum((out_tables[i]['dp'] - dp_mean) ** 2) / (N * (N - 1))) ** 0.5  # (19)
    out_tables[i]['dw_inac'] = t_stu * (
            sum((out_tables[i]['dwe'] - dw_mean) ** 2) / (N * (N - 1))) ** 0.5  # (19)

with pd.ExcelWriter('out/task1.xlsx') as writer:
    for i in range(7, 11):
        table = pd.DataFrame(out_tables[i])
        table.to_excel(writer, sheet_name=f"Table{i}", index=False)
