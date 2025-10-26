import numpy as np
import matplotlib.pyplot as plt
from SpheriCalc import SpheriCalc
from line_interpolation import line_interpolate


sph_calc = SpheriCalc(n2=1.5, s1=-50, n1=1, r=30)
# print(sph_calc.q1)
# print(sph_calc.q2)
# print(sph_calc.f1)
# print(sph_calc.f2)
# print(sph_calc.beta)
# print(sph_calc.gamma)
# print(sph_calc.alpha)
# print(sph_calc)

# sph_calc01 = SpheriCalc(n1=1.0, n2=1.5, s1=-35, r=10)
sph_calc01 = SpheriCalc(n1=1.33, n2=1.0, s1=-10, r=-30)
print(sph_calc01)

n1 = sph_calc01.n1
n2 = sph_calc01.n2
s1 = sph_calc01.s1
s2 = sph_calc01.s2
f1 = sph_calc01.f1
f2 = sph_calc01.f2
r = sph_calc01.r
beta = sph_calc01.beta
gamma = sph_calc01.gamma
alpha = sph_calc01.alpha
q1 = sph_calc01.q1
q2 = sph_calc01.q2

y1 = 1.0
y2 = beta * y1

ymin, ymax = min(y1, y2) - 10, max(y1, y2) + 10
xmin, xmax = min(s1, s2, f1, f2, 0) - 10, max(s1, s2, f1, f2, 0) + 10

fig, ax = plt.subplots(ncols=1, nrows=1)
ax.grid()
if n1 < n2:
    ax.fill_between([0, xmax], ymin, ymax, color='tab:gray', alpha=0.2)
elif n1 > n2:
    ax.fill_between([xmin, 0], ymin, ymax, color='tab:gray', alpha=0.2)
#ax.axhline(0, color='black', linewidth=0.5)
#ax.axvline(0, color='black', linewidth=0.5)
if s1 < 0:
    ax.plot([s1, s1], [0, y1], '-', color='tab:blue')  # Object height
elif s1 > 0:
    ax.plot([s1, s1], [0, y1], '--', color='tab:blue')  # Object height
if s2 > 0:
    ax.plot([s2, s2], [0, y2], '-', color='tab:orange')  # Image height
elif s2 < 0:
    ax.plot([s2, s2], [0, y2], '--', color='tab:orange')  # Image height
ax.plot([0, 0], [ymin, ymax], '-', color='black')  # Surface
ax.plot([xmin, xmax], [0, 0], '-.', color='black')  # Optical axis

ax.plot([f1, f1], [ymin, ymax], '--', color='tab:gray')  # Object focal plane
ax.plot(f1, 0, 'o', color='tab:gray')
ax.text(f1 + 0.5, 0.5, "F", color='tab:gray')
ax.plot([f2, f2], [ymin, ymax], '--', color='tab:gray')  ## Image focal plane
ax.plot(f2, 0, 'o', color='tab:gray')
ax.text(f2 + 0.5, 0.5, "F'", color='tab:gray')
ax.plot(r, 0, 'o', color='tab:red')
ax.text(r + 0.5, 0.5, "C", color='tab:red')

# Rays
if s1 < 0:
    ax.plot([s1, 0], [y1, y1], '-', color='black')
    ax.plot(*line_interpolate(s1, y1, r, 0, s1, 0), '-', color='black')
    ax.plot(*line_interpolate(s1, y1, f1, 0, s1, 0), '-', color='black')
ax.plot(*line_interpolate(0, y1, f2, 0, 0, xmax), '-', color='black')
ax.plot(*line_interpolate(r, 0, s2, y2, 0, xmax), '-', color='black')
ax.plot([0, xmax], [y2, y2], '-', color='black')
if s2 < 0:
    ax.plot([s2, 0], [y2, y1], '--', color='black')
    ax.plot([s2, 0], [y2, y2], '--', color='black')
    ax.plot(*line_interpolate(s2, y2, r, 0, s2, 0), '--', color='black')
if s1 > 0:
    ax.plot([xmin, 0], [y1, y1], '-', color='tab:red')
    ax.plot(*line_interpolate(f1, 0, s1, y1, xmin, 0), '-', color='tab:red')
    ax.plot(*line_interpolate(r, 0, s1, y1, xmin, 0), '-', color='tab:red')

    ax.plot([0, s1], [y1, y1], '--', color='tab:red')
    ax.plot(*line_interpolate(f1, 0, s1, y1, 0, s1), '--', color='tab:red')
    ax.plot(*line_interpolate(r, 0, s1, y1, 0, s1), '--', color='tab:red')

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
#print(min(y1, y2) - 10, max(y1, y2) + 10)
plt.show()
