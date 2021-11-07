import sympy as sy
import numpy as np
x, y, x2, y2, n1, n3, n5 = sy.symbols('x, y, x2,y2, n1, n3, n5')

eq = [x-n1/n5*y, x2-n3/n5*y2, -x + x2 + y2, x+y-1, x - 1/60, x2 - 1/(12*60)]


r = sy.nonlinsolve(eq, [x, y, x2, y2, n1, n3, n5])
r2 = np.array(r.args[0][-3:])
print(r2*59)
print(1/r2)
xar = 0.001
n = np.arange(1, 100, 1)
for i in n:
    ro = [ni.subs(n5, 59*i) for ni in r2]
    n2 = (ro[2]-ro[0])/2
    n4 = (ro[2]-ro[1])/2
    r3 = ro + [n2, n4]
    if any([np.abs(xii - round(xii)) > xar for xii in r3]):
        continue

    r34 = np.pi / np.array([np.arcsin(float((r3[3] + 2) / (r3[3] + r3[0]))), np.arcsin(float((r3[4] + 2) / (r3[4] + r3[1])))])
    r3.extend([r34, (+r3[3]+r3[0])/2, (r3[4]+r3[1])/2])
    r3 = [str(xi) for xi in r3]

    print(', '.join(r3))

