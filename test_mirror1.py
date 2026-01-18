from opticalc import MirrorCalc
import matplotlib.pyplot as plt


mirror_calc = MirrorCalc(s1=None, s2='inf', r=30)
print(mirror_calc)
fig = mirror_calc.plot1(aspect_equal=True)
plt.show()