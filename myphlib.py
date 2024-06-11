import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def measure_sko(vel: pd.Series):
    return ((vel - vel.mean()) ** 2) / (len(vel) * (len(vel) - 1))


def save(name: str, module):
    module.legend()
    module.savefig("out/" + name + '.png', dpi=500)
    module.show()


def save_tables(name, out_table, indexes):
    with pd.ExcelWriter('out/' + name + '.xlsx') as writer:
        for table_index in indexes:
            table = pd.DataFrame(out_table[table_index])
            table.to_excel(writer, sheet_name=f"Table{table_index}")


class MNK:
    def __init__(self, x: pd.Series, y: pd.Series):
        x = pd.Series(x)
        y = pd.Series(y)
        self.N = len(x)
        self.a = (sum((x - x.mean()) * (y - y.mean())) / sum((x - x.mean()) ** 2))
        self.b = y.mean() - self.a * x.mean()
        self.y_new = list(map((lambda _: self.b + self.a * _), x))
        self.d = (y - (self.b + self.a * x))
        self.D = sum((x - x.mean()) ** 2)
        self.sko_b = sum(self.d ** 2) / (self.D * (self.N - 2))
        self.sko_a = sum(self.d ** 2) / (self.N - 2) * (1 / self.N + (x.mean() ** 2) / self.D)
        self.a_inac = 2 * self.sko_a
        self.b_inac = 2 * self.sko_b
        self.y_inac = ((2 * self.b * x.max()) ** 2 + (2 * self.a) ** 2) ** 0.5
