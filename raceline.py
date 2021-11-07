import numpy as np
import sympy as sy
import pandas as pd
from scipy.optimize import minimize

print(f'\nRaceLine Calculations\n\n')

# symbols
t0, t1, red, s2, vt = sy.symbols("t0, t1, red, s2, vt")

# constants
init_red = 2.7
fin_red = 1
power = 24.4e3
m = 200
mu = 0.7
eng_sp = 6500  # rpm
g = 9.81
tire_rad = 0.180
track_width = 26.6

# list fof all turns
turn_array = [[215, 1644],
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


def race_line(min_rad, max_rad, arc_ang):
    # calculates the raceline (max radius given width of track) for a turn
    cos_a = np.cos(np.deg2rad(arc_ang / 2))
    return (max_rad - min_rad * cos_a) / (1 - cos_a)


def find_r(arc_len, rad_cen):
    # if track is given as width and center radius insted of max, min radius

    ang = arc_len / rad_cen  # angle given arc
    min_rad = rad_cen - track_width
    max_rad = rad_cen + track_width
    ra = 12 * 0.0254  # ft to m
    return [min_rad * ra, max_rad * ra, np.rad2deg(ang)]


def by_ex(ratio_ls, cnt, defined_ratios=None):
    # calculates optimal ratios given number of gears, some preset ratios and optimal ratios for each turn
    def optimize(guess):
        # function for scipy to optomizes since we want the gear ratios where we have each turn be the closest to a gear
        defined_guess = np.sort(np.concatenate((guess, defined_ratios)))  # if some ratios are set
        cost = 0
        for turn in ratio_ls:
            # minds the optimal ratio for each turn, scypi will find min diff
            cost += np.min(np.abs(defined_guess - turn))
        return cost

    if defined_ratios:
        cnt -= len(defined_ratios)
    else:
        defined_ratios = []
    ratio_ls.sort()
    out_r = np.linspace(ratio_ls[0], ratio_ls[-1], cnt)  # initial guess
    result = minimize(optimize, out_r, options={'disp': False})
    return result.x  # function can return iterations, only need output


# turn radius array [min, max, arc_angle] or [arc_len, center rad]
if len(turn_array[0]) == 2:  # see if need to convert to min max
    turn_array_norm = [find_r(*turn_n) for turn_n in turn_array]
else:
    turn_array_norm = turn_array
    
rad_array = np.array(turn_array_norm)
rad_array = np.hstack((rad_array, np.zeros([rad_array.shape[0], 3])))  # shape correctly

# full drivetrain redux
total_r = red * init_red * fin_red

# loops through each turn and calculates all values
for i in range(rad_array.shape[0]):
    rad = race_line(*rad_array[i, :3])  # finds the optimale raceline for each turn
    # all eqs in the form x-y = 0,

    t_eq = [t0 - power / eng_sp,  # find initial torque
            s2 - eng_sp / total_r,  # find output speed (solving for red)
            vt - np.sqrt(g * mu * rad),  # vt from turn (acc_n*m = v^2/r, and acc_n*m <= Fric_F)
            vt - tire_rad * s2 * np.pi / 30  # vt = out speed * r, convering rpm to rad/s
            ]

    sol = sy.nonlinsolve(t_eq, [red, s2, t0, vt])  # soving system
    rad_array[i, 3:] = [rad, sol.args[0][3], sol.args[0][0]]  # used to get v and gear ratios

# creats dataframe of values for pretty print or saving
df = pd.DataFrame(rad_array, columns=["min", "max", "deg", "race", "v", "R"])
print(df)

# calculates optimal gear ratios based on turns
rat = by_ex(list(df['R']), 4)
print(f'\nOptimal ratios for track are: {rat}\n')
