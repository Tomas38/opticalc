import numpy as np
from opticalc.spheri_calc import SpheriCalc


sph_calc = SpheriCalc(n2=1.5, s1=-50, n1=1, r=30, s2=None)
# print(sph_calc.q1)
# print(sph_calc.q2)
# print(sph_calc.f1)
# print(sph_calc.f2)
# print(sph_calc.beta)
# print(sph_calc.gamma)
# print(sph_calc.alpha)
# print(sph_calc)

sph_calc01 = SpheriCalc(n1=1.0, n2=1.5, s1='inf', r=10, s2=None)
print(sph_calc01)

# Test case when image lies in the focal plane
sph_calc02 = SpheriCalc(n1=1.0, n2=1.5, s2=30, r=10, s1=None)
print(sph_calc02)

# Test case when refractive indices are equal
sph_calc03 = SpheriCalc(n1=1.0, n2=1.0, s2=30, r=10, s1=None)
print(sph_calc03)

# Test case when refractive indices are equal
sph_calc04 = SpheriCalc(n1=1.0, n2=1.5, s1=-35, r=10, s2=None)
print(sph_calc04)


sph_calc05 = SpheriCalc(n1=1, n2=1.6, s1='-inf', r=15, s2=None)
print(sph_calc05)

sph_calc06 = SpheriCalc(n1=1, n2=1.6, s1=-1e6, r=15, s2=None)
print(sph_calc06)

sph_calc07 = SpheriCalc(n1=1.0000001, n2=1.000, s2=-1e15, r=15, s1=None)
print(sph_calc07)

sph_calc08 = SpheriCalc(n1=1, n2=1.0, s1=np.inf, r=15, s2=None)
print(sph_calc08)

sph_calc09 = SpheriCalc(n1=1, n2=1.0, s2=np.inf, r=15, s1=None)
print(sph_calc09)

sph_calc10 = SpheriCalc(n1=1.5, n2=1.0, s1=np.inf, r=-1e10, s2=None)
print(sph_calc10)

sph_calc11 = SpheriCalc(n1=1.5, n2=1.0, s1=np.inf, s2=np.inf, r=None)
print(sph_calc11)