import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from opticalc import SpheriCalc

# sph_calc = SpheriCalc(
#             n1=1.0,
#             n2=1.5,
#             s1='inf',
#             r=-0.001,
#             s2=None,
#         )
# print(sph_calc)


# Initial parameter values
INIT = {
    'n1': 1.00,
    'n2': 1.52,
    's1': -12.0,
    'r': 3.0,
}

INIT = {
    'n1': 1.0,
    'n2': 1.5,
    's1': 2.0,
    'r': -1.0,
}


fig, ax = plt.subplots(figsize=(10, 4))
plt.subplots_adjust(left=0.08, right=0.98, bottom=0.32, top=0.95)


def draw_system(_: float | None = None) -> None:
    """Recompute the optical system and redraw the plot when a slider changes."""
    ax.clear()
    try:
        sph_calc = SpheriCalc(
            n1=slider_n1.val,
            n2=slider_n2.val,
            s1=slider_s1.val,
            r=slider_r.val,
            s2=None,
        )
        sph_calc.plot1(
            ax=ax,
            ylim=(-4, 4),
            xlim=(-25, 25),
            object_height=1,
            fill_medium=True,
            surface_as_arc=True,
            aspect_equal=False,
        )
        ax.set_title(
            f"s1={sph_calc.s1:.2f}, n1={sph_calc.n1:.2f}, n2={sph_calc.n2:.2f}, r={sph_calc.r:.2f}"
        )
    except Exception as exc:
        # Show validation errors directly on the plot instead of crashing.
        ax.text(0.5, 0.5, str(exc), ha='center', va='center', transform=ax.transAxes, color='red')
    fig.canvas.draw_idle()


# Slider axes
slider_height = 0.03
slider_spacing = 0.01
base_bottom = 0.08
ax_s1 = fig.add_axes((0.12, base_bottom + 3 * (slider_height + slider_spacing), 0.76, slider_height))
ax_n1 = fig.add_axes((0.12, base_bottom + 2 * (slider_height + slider_spacing), 0.76, slider_height))
ax_n2 = fig.add_axes((0.12, base_bottom + 1 * (slider_height + slider_spacing), 0.76, slider_height))
ax_r  = fig.add_axes((0.12, base_bottom + 0 * (slider_height + slider_spacing), 0.76, slider_height))


# Sliders
slider_s1 = Slider(ax_s1, 's1', valmin=-40.0, valmax=40.0, valinit=INIT['s1'], valstep=0.1)
slider_n1 = Slider(ax_n1, 'n1', valmin=1.0, valmax=2.5, valinit=INIT['n1'], valstep=0.01)
slider_n2 = Slider(ax_n2, 'n2', valmin=1.0, valmax=2.5, valinit=INIT['n2'], valstep=0.01)
slider_r = Slider(ax_r, 'r', valmin=-20.0, valmax=20.0, valinit=INIT['r'], valstep=0.1)

slider_s1.on_changed(draw_system)
slider_n1.on_changed(draw_system)
slider_n2.on_changed(draw_system)
slider_r.on_changed(draw_system)


draw_system()
plt.show()
