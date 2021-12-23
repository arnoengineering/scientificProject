import numpy as np
import sympy as sy
import random

mu = 0.7
g = 9.81
k_max = 2  # turn rad of car
v_max = 100
turns = 100
ds = 1.4 / 100  # dis
# x, y = sy.symbols('x y')

cv = np.array([[0, 1],
               [0, 1]])

xc = cv[:, 0]
yc = cv[:, 1]


def dx(x, i):
    return x[i] - x[i - 1]


def dy(y, i):
    return y[i] - y[i - 1]


def k(x, y, i):
    if dx(x, i) == 0:
        return 0
    else:
        return (dy(y, i) / dx(x, i)) / (1 + (dy(y, i) / dx(x, i)) ** 2) ** 1.5


def cent_d(x, y, i):
    return np.norm((x[i] - xc[i], y[i] - yc[i]))


def cent_c(x, y, i):
    return xc[i] * (x[i] - xc[i]) + yc[i] * (y[i] - yc[i])


def dist(p1, p2):
    return np.norm(p2-p1)  # asumming both np arrays should work,
    # todo switch so angle and dist, given by ds


kc = [k(x, y, i) for i, x, y in enumerate(zip(xc, yc))]
kc_m = np.max(kc)


def find_var(s):
    p = random.random()
    return (-1+np.sqrt(1-s*(2-s-4*p)))/s


def find_s(i):
    return min(max((kc[i+1]-kc[i])/kc_m, -1), 1)


def t_i(x, y, i):
    return 1 / np.sqrt(g * mu) * k(x, y, i)  # todo add turn constraints

ls_ls = []
for ii in range(1000):
    t = 0
    for iii in turns
ls = []