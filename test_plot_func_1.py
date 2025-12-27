import matplotlib.pyplot as plt
from opticalc import SpheriCalc


# Example usage
#sph_calc01 = SpheriCalc(n1=1.33, n2=1.0, s1=-50, r=-30)
#sph_calc01 = SpheriCalc(n1=1.0, n2=1.5, s1=25, r=-10)
sph_calc01 = SpheriCalc(n1=1.5, n2=1.0, s1=-20, r=-10, s2=None)
sph_calc01 = SpheriCalc(n1=1.33, n2=1.0, s1=-4, r=-3, s2=None)
print(sph_calc01)
fig1 = sph_calc01.plot1()
plt.show()
