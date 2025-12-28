import matplotlib.pyplot as plt
from opticalc import SpheriCalc


# Define your s1 values to iterate through
s1_values = [-20, -10, -4, -3, 2, 20]

# Create subplots grid
fig, axs = plt.subplots(3, 2, figsize=(12, 8))
axs = axs.flatten()  # Flatten to easily iterate

# Create multiple plots using a for loop
for i, s1 in enumerate(s1_values):
    sph_calc = SpheriCalc(n1=1.00, n2=1.52, s1=s1, r=+3, s2=None)
    #rint(f"\ns1 = {s1}:")
    #print(sph_calc)
    
    # Pass the axis to plot1
    sph_calc.plot1(xlim=(-25, 25),
                   ax=axs[i],
                   #ylim=(-5, 5),
                   object_height=5,
                   fill_medium=True,
                   surface_as_arc=False,
                   aspect_equal=False)
    #axs[i].set_title(f's1 = {s1}')
    #axs[i].set_ylim(-5, 5)
    #axs[i].set_aspect(10)

fig.tight_layout()
plt.show()
