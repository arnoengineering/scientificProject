import itertools
import pandas as pd
import numpy as np


df = pd.read_excel("gear.xlsx", 1)

# center distace range
range_t = np.arange(50, 85, 1)
ra = 0.01
range_d = [15, 30]
df_f = df[range_d[0] <= df["For Shaft Dia"]]
df_f = df_f[df_f["For Shaft Dia"] <= range_d[1]]
df_l = {}
df_li = []
data_f_index = []
f_o_n = 'outpot_gear_op.xlsx'
out_l = ["Gear PitchDia", "Part N L", "For Shaft Dia"]


def comb(n):
    for i in itertools.combinations(range(len(df_f)), 2):
        # print(i)
        d_f_i = df_f.iloc[list(i)]
        if np.abs(np.sum(d_f_i["Gear PitchDia"])/2-n) <= ra:
            ri = list(d_f_i["Gear PitchDia"])
            r = round(ri[1]/ri[0], 5)
            # keys
            ris = d_f_i[out_l].values.tolist()
            # ris = ris[0]
            # print(ris)
            ris_3 = [r] + ris[0] + [round(1/r, 5)] + ris[1]
            # print(ris_3)
            # df_li.append(ris_3)
            if n not in df_l.keys():
                df_l[n] = []
            df_l[n].append(ris_3)
            # df


if __name__ == '__main__':
    for ii in range_t:
        print(ii)
        comb(ii)

for x, ii in df_l.items():
    li = len(ii)
    if li >= 4:
        # df_f2[x] = ii
        for ite in range(li):
            df_li.append(ii[ite])
            data_f_index.append((x, ite))

index = pd.MultiIndex.from_tuples(data_f_index)
coloum = pd.MultiIndex.from_product([["Gear1", "Gear2"], ["ratio"] + out_l])
# df_f2 = {x: ii for x, ii in  if len(ii) >= 4}

dn = pd.DataFrame(np.array(df_li), index=index, columns=coloum)
print(dn)

dn.to_excel(f_o_n)
# print(df_f2[55])
