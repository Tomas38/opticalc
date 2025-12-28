import matplotlib.pyplot as plt
from opticalc import SpheriCalc

# Create subplots grid
fig, ax = plt.subplots(1, 1, figsize=(10, 4))

sph_calc = SpheriCalc(n1=1.00, n2=1.52, s1=-12, r=+3, s2=None)
sph_calc = SpheriCalc(n1=1.52, n2=1.00, s1=-12, r=+3, s2=None)
sph_calc = SpheriCalc(n1=1.52, n2=1.00, s1=0.0, r=+3, s2=None)
print(sph_calc)
    #rint(f"\ns1 = {s1}:")
    #print(sph_calc)
    
    # Pass the axis to plot1
sph_calc.plot1(#xlim=(-25, 25),
                ax=ax,
                ylim=(-3, 3),
                object_height=1,
                fill_medium=True,
                surface_as_arc=True,
                aspect_equal=True)
    #axs[i].set_title(f's1 = {s1}')
    #axs[i].set_ylim(-5, 5)
    #axs[i].set_aspect(10)

fig.tight_layout()
plt.show()
