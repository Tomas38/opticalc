from opticalc import SpheriCalc


sph_calc = SpheriCalc(n2=1.5, s1=-50, n1=1, r=30, s2=None)
# print(sph_calc.q1)
# print(sph_calc.q2)
# print(sph_calc.f1)
# print(sph_calc.f2)
# print(sph_calc.beta)
# print(sph_calc.gamma)
# print(sph_calc.alpha)
# print(sph_calc)

print(sph_calc)

sph_calc71a = SpheriCalc(n1=1, n2=1.6, s1=-50, r=15, s2=None)
print(sph_calc71a)
sph_calc71b = SpheriCalc(n1=1, n2=1.6, s1=+50, r=15, s2=None)
print(sph_calc71b)

# self.beta = (self.n1 / self.n2) * (self.s2 / self.s1)
s1 = (1.0 / 1.6) * 40 / 4
sph_calc72 = SpheriCalc(n1=1, n2=1.6, s2=+40, s1=s1, r=None)
print(sph_calc72)

sph_calc73 = SpheriCalc(n1=1.0, s1='inf', s2=20, r=10, n2=None)
print(sph_calc73)

sph_calc75 = SpheriCalc(n1=1.6, n2=1.0, s2=-5, r=-3, s1=None)
print(sph_calc75)

sph_calc73r = SpheriCalc(n2=1.0, s2='inf', s1=-20, r=-10, n1=None)
print(sph_calc73r)

sph_calc01 = SpheriCalc(n1=1.0, n2=1.5, s1='inf', r=10, s2=None)
print(sph_calc01)

# Test case when image lies in the focal plane
sph_calc02 = SpheriCalc(n1=1.0, n2=1.5, s2=30, r=10, s1=None)
print(sph_calc02)
