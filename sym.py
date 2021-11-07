import numpy as np
import sympy as sy
from sympy import init_printing
from sympy import integrate
from sympy import SingularityFunction as sf
from sympy.physics.vector import *
import matplotlib.pyplot as plt
# from sympy.printing import *
# from IPython.display import display, Latex

from sympy.printing import latex
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
"""add solution and relation equations, add relivant tables from
add logical vars and prints
plot track, plot sigularty, solve for stresses, add database"""
# car,
g = 9.81
kr_val = {}
e_r = [205, 7.85]
init_printing()

x = sy.Symbol('x', positive=True)


def print_l(st):
    a = latex(st)
    ax = plt.subplot(111)# left,bottom,width,height
    ax.set_xticks([])
    # plt.ylabel()
    ax.axis('off')
    te = f'${a}$'
    plt.text(0.4, 0.4, te, size=50, color="g")
    plt.show()


    # display(Latex())


class car:
    def __init__(self):
        self.m = 200


car_ref = ReferenceFrame('car')
gear_ref = ReferenceFrame('gear')


class gear:
    def __init__(self, g_ind, m=None, loc=None, d=None, ia=None):
        self.m = m if m else sy.symbols(f'G{g_ind}m')
        self.loc = loc if loc else sy.symbols(f'G{g_ind}loc')
        self.d = d if d else sy.symbols(f'G{g_ind}g_d')
        self.r = d / 2
        self.I = ia if ia else m * self.r ** 2  # todo add fornce
        # self.
        self.N, self.fx = sy.symbols(f'G{g_ind}N G{g_ind}fx')  # todo add name


class bearing:
    def __init__(self, m, loc, kr, a, life, inde=0):
        self.life_span = life * 1e6
        self.m = m
        self.kr = kr
        self.a = a
        self.loc = loc * gear_ref.y
        self.loadx, self.loadz, self.d = sy.symbols(f'B{inde}p_x B{inde}p_z B{inde}d')
        self.fric = 0.2  # todo change ass

        self.load = self.loadx * gear_ref.x + self.loadz * gear_ref.z
        self.fric_f = self.load * self.fric * self.d

    def find_c(self):
        kr = kr_val[self.kr]  # find in table
        c = self.load * (self.life_span / kr) ** (1 / self.a)


def it(f):
    return integrate(f, x)


def gen_st(va, cnt):
    st = ""
    for ii in range(cnt):
        st += va + str(ii) + " "
    return sy.symbols(st)


def moment(m, a):
    return m * sf(x, a, -2)


def point_load(f, a):
    return f * sf(x, a, -1)


def dis_load(f, a, b):
    ave_f = f / (a - b)
    return ave_f * sf(x, a, 1) - ave_f * sf(x, b, 1) - f * sf(x, b, 0)


def con_load(f, a, b):
    return f * sf(x, a, 0) - f * sf(x, b, 0)


d_mat = np.array([10, 20, 30, 40, 40, 30, 20, 10])

gears = np.array([gear(n, m=0.1, loc=0.1 * (n % 4), d=d) for n, d in enumerate(d_mat)]).reshape((2, 4))
bearings = np.array([bearing(0.5, n, 0.1, 3, 3) for n in [0, 1, 0, 1]]).reshape((2, 2))


class beam:
    def __init__(self, gear_l, bear, e_ro, nor=1):
        self.E = e_ro[0]
        self.ro = e_ro[1]

        ind = 1 if nor == 1 else 2
        self.d, self.c1, self.c2, self.om, self.al = sy.symbols(f'b{ind}d b{ind}c1 b{ind}c2 b{ind}om b{ind}alpha')
        self.gear_v = []

        self.len = 1  # todo change
        self.i = sy.symbols('b{ind}I')  # todo calc I
        self.bear = bear

        self.gear_l = gear_l
        self.m = self.ro * self.len * self.d ** 2 / 4 * np.pi
        self.w = self.m * g
        self.internal_relat_eq = []
        self.nor = nor
        # r locs or constant
        # test if ger giving  torque

        self.mom_list = []
        self.force_list = []

        # self.sum_f_l = [[], [], []]
        # self.sum_m_l = [[], [], []]
        self.sum_f = [0, 0, 0]
        self.sum_m = [0, 0, 0]
        self.cond = [[0, 0, 0],  # find extra vals
                     [0, self.i * self.al, 0]]

    def run_f(self, ex_f, m_ex):
        for n, ge in enumerate(self.gear_l):
            self.gear_v.extend([ge.N, ge.fx])
            fl = ge.r * gear_ref.z + ge.loc * gear_ref.y
            norm = -self.nor * gear_ref.z * ge.N
            fx = self.nor * gear_ref.x * ge.fx
            fg = fx + norm
            self.append_l(fl, fg)

        for n, f in ex_f:
            # n is len
            self.append_l(n, f)

        for n, m in m_ex:
            self.mom_list.append([n * gear_ref.y, m * gear_ref.y])

        for b in self.bear:
            # self.gear_v.append(b.load)
            self.internal_relat_eq.append(self.d-b.d)
            self.append_l(b.loc, b.load)
            self.mom_list.append([b.loc, b.fric_f])

        self.sum_f = np.sum([n[1].to_matrix(gear_ref) for n in self.force_list])
        self.sum_m = np.sum([n[1].to_matrix(gear_ref) for n in self.mom_list])
        print('f')
        print_l(self.sum_f)
        print('mom')
        print_l(self.sum_m)

    def append_l(self, l1, l2):
        fli = [l1, l2]
        self.force_list.append(fli)
        self.mom_list.append([fli[0], cross(*fli)])

    def gen_sing(self, ax):  # todo swap for ax, l along other
        q = 0
        q += dis_load(self.w, 0, self.len)
        for n in self.force_list:
            loc = n[0].to_matrix(gear_ref)[1]  # y
            f = n[1].to_matrix(gear_ref)[ax]
            q += point_load(f, loc)
        for m in self.mom_list:
            loc = m[0].to_matrix(gear_ref)[1]  # y
            f = m[1].to_matrix(gear_ref)[(ax + 2) % 4]
            q += moment(f, loc)

        v = it(q)
        M = it(v)
        # th = it(M / (self.E * self.i)) + self.c1
        # deflec = it(th) + self.c2  # todo add bound for deflec = 0, plot eqs
        print_l(q)
        print_l(M)

    def min_d(self):
        # guess d =
        d_0 = 0
        # while d_0 <0:
        #     # do x
        # add to eq


# glomal eq = list all eq in each also relative eq and add a, v and chech if f<N*0.7
# w rel same forces,
b1 = beam(gears[0], bearings[0], e_r)
b2 = beam(gears[1], bearings[1], e_r, -1)
t_in = [[0, 10]]
t_out = [[1, 5]]
b1.run_f([], t_in)
b2.run_f([], t_out)
b1.gen_sing(2)

# add wheel
# add engine t in and t out
ni = 1  # temp g rat
rel_eq = [b2.om + b1.om * ni, b1.al - +b2.al * ni]
for i, j in zip(b1.gear_v, b2.gear_v):
    rel_eq.append([i - j])  # m=m2, x=x2

print(rel_eq)
