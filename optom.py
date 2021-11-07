import numpy as np
from scipy.optimize import minimize


def by_ex(in_ls, cnt):
    def optimize(gess):
        cost = np.zeros(len(in_ls))
        # print(in_ls)
        # print(gess)
        # print()
        for i, n in enumerate(in_ls):
            cost[i] = np.min(np.abs(gess - n))
        cost_f = sum(cost)
        return cost_f
    in_ls.sort()
    out_r = np.linspace(in_ls[0], in_ls[-1], cnt)
    result = minimize(optimize, out_r, options={'disp': False})
    return result.x
