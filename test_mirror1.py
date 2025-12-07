from opticalc import MirrorCalc
import matplotlib.pyplot as plt


mirror_calc = MirrorCalc(s1=-20, s2=None, r=-30)
print(mirror_calc)
fig = mirror_calc.plot1()
plt.show()