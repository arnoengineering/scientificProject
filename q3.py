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
E = 504e9
x = sy.Symbol('x', positive=True)
c = np.array([sy.Symbol('c1y c2y'), sy.Symbol('c1z c2z')])


def print_l(st):
    a = latex(st)
    ax = plt.subplot(111)  # left,bottom,width,height
    ax.set_xticks([])
    # plt.ylabel()
    ax.axis('off')
    te = f'${a}$'
    plt.text(0.4, 0.4, te, size=50, color="g")
    plt.show()

    # display(Latex())


car_ref = ReferenceFrame('car')
gear_ref = ReferenceFrame('gear')
engine_t = 2.4 * 1000 / (6500 * np.pi / 30)
gear_loc = np.array([0, 80, 185, 312, 355]) * 0.001
gear_forces = [1, 2, 3, 4]
gear_r = np.array([[60, 80, 100, 120], [180, 160, 140, 120]]) * 0.001
L = gear_loc[-1]
step_loc = np.array([0, 170, 297, L]) * 0.001
d = 0.045


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


def tot(jj):
    return sy.sqrt(jj[0] ** 2 + jj[1] ** 2)

def sol_v(ar, tf):
    return [float(ar.subs(x, tt)) for tt in tf]
# add wheel
# add engine t in and t out
tr = np.linspace(0, L, 100)
titlel = ['Q', 'v', 'M', 'th', 'del']
for i in range(1):  # todo change after debug
    gearf = engine_t * gear_r[0, i]
    g_fr = gearf * np.tan(np.deg2rad(20))
    loc = gear_loc[i + 1]
    g_l = np.array([gearf, g_fr])
    r2 = g_l * loc / L
    r1 = g_l - r2
    Qeq = sy.zeros(5, 2)
    Q_t = []
    # v=[]
    # M=[]
    # delt=[]
    # th = []
    for j in range(2):
        Qeq[0, j] = point_load(r1[j], 0) + point_load(r2[j], L) - point_load(g_l[j], loc)
        for ii in range(4):
            Qeq[ii + 1, j] = it(Qeq[ii,j])

        # th.append(it(M[j]))# + c1.. todo solve
        # delt.append(it(th[j]))
    fig, ax = plt.subplots(2,2)
    for row in range(Qeq.rows):
        ri = row % 2
        if row>1:
            rii =1
        else:
            rii=0
        jjj = Qeq.row(row)
        jj_t = tot(jjj)

        Q_t.append(jj_t)
        ax[rii, ri].plot(tr*1000, sol_v(jjj[0],tr))
        ax[rii, ri].plot(tr*1000, sol_v(jjj[1],tr))
        ax[rii, ri].plot(tr*1000, sol_v(jj_t,tr))
        ax[rii, ri].legend(['y','z','|titlel[row]|'])
        ax[rii, ri].set_title(titlel[row])
plt.show()
    # ax, fig = plt.subplot()
    # fig.plot(tr, ) todo plot individuals, and sum
