import matplotlib.pyplot as plt
from opticalc import SpheriCalc


# Example usage
sph_calc01 = SpheriCalc(n1=1.0, n2=1.52, s1=-50, r=-35, s2=None)
print(sph_calc01)

s1_2 = sph_calc01.s2 - 2.5
sph_calc01 = SpheriCalc(n1=1.52, n2=1.0, s1=s1_2, r=-8, s2=None)
print(sph_calc01)
fig1 = sph_calc01.plot1()
fig2 = sph_calc01.plot2()
plt.show()
