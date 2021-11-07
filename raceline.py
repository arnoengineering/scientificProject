import numpy as np
import sympy as sy
import pandas as pd
from optom import by_ex


def race_line(r1, r2, deg):
    return (r2 - r1 * np.cos(np.deg2rad(deg / 2))) / (1 - np.cos(np.deg2rad(deg / 2)))


print(f'\nRaceLine Calculations\n\n')
# constants
init_red = 2.7
fin_red = 1
power = 24.4 * 10 ** 3
m = 200
mu = 0.7
eng_sp = 6500  # rpm
g = 9.81
tire_rad = 0.180

# symbols
t0, t1, red, s2, vt = sy.symbols("t0, t1, red, s2, vt")


def find_r(a,r):
    l = 26.6
    ang=a/r
    r1=r-l
    r2=r+l
    ra=12*0.0254
    return [r1*ra, r2*ra, np.rad2deg(ang)]


# full drivetrain redux
total_r = red * init_red * fin_red
n=[[215, 1644],
[227, 120],
[296, 270],
[208, 679],
[177, 298],
[280, 907],
[167, 137],
[494, 358],
[158, 100],
[89, 106],
[176, 309],
[118, 1159],
[173, 2889],
[219, 444],
[130, 277],
[338, 2000],
[328, 168],
[284, 552],
[228, 375],
[315, 300],
[251, 300],
[105, 149],
[97, 105],
[90, 105],
[94, 290],
[226, 134],
[162, 201],
[220, 596],
[337, 423],
[175, 165],
[299, 727],
[92, 165],
[200, 950],
[693, 1375]]

# turn radius array [min, max, arc]
rad_array = np.array([find_r(*n2) for n2 in n])

rad_array = np.hstack((rad_array, np.zeros([rad_array.shape[0], 3])))  # shape correctly

# loops through each turn and calculats all values
for i in range(rad_array.shape[0]):
    rad = race_line(*rad_array[i, :3])
    t_eq = [t0 - power / eng_sp, s2 - eng_sp / total_r, vt - np.sqrt(g * mu * rad), vt - tire_rad * s2 * np.pi / 30]
    sol = sy.nonlinsolve(t_eq, [red, s2, t0, vt])
    rad_array[i, 3:] = [rad, sol.args[0][3], sol.args[0][0]]

# creats dataframe of values for pretty print or saving
df = pd.DataFrame(rad_array, columns=["min", "max", "deg", "race", "v", "R"])
print(df)

# calculates optimal gear ratios based on turns
rat = by_ex(list(df['R']), 4)
print(f'\nOptimal ratios for track are: {rat}\n')
