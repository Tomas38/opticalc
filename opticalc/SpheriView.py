import numpy as np
import matplotlib.pyplot as plt
from SpheriCalc import SpheriCalc
from line_interpolation import line_interpolate


class SpheriView:
    def __init__(self):
        pass

    def __new__(self, spheri_calc):
        self.spheri_calc = spheri_calc
        self.n1 = self.spheri_calc.n1
        self.n2 = self.spheri_calc.n2
        self.s1 = self.spheri_calc.s1
        self.s2 = self.spheri_calc.s2
        self.f1 = self.spheri_calc.f1
        self.f2 = self.spheri_calc.f2
        self.r = self.spheri_calc.r
        self.beta = self.spheri_calc.beta
        self.gamma = self.spheri_calc.gamma
        self.alpha = self.spheri_calc.alpha
        self.q1 = self.spheri_calc.q1
        self.q2 = self.spheri_calc.q2

        y1 = 10.0
        y2 = self.beta * y1

        y_offset = max(abs(y1), abs(y2)) * 0.3
        x_offset = max(abs(self.s1), abs(self.s2), abs(self.f1), abs(self.f2), 10) * 0.2
        ymin, ymax = min(y1, y2, 0) - y_offset, max(y1, y2, 0) + y_offset
        xmin, xmax = min(self.s1, self.s2, self.f1, self.f2, 0) - x_offset, max(self.s1, self.s2, self.f1, self.f2, 0) + x_offset
        
        # Fix to have optical axis in the middle
        ylim = max(abs(ymin), abs(ymax))
        ymax = ylim
        ymin = -ylim

        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8, 3))
        # ax.grid()
        if self.n1 < self.n2:
            ax.fill_between([0, xmax], ymin, ymax, color='tab:gray', alpha=0.2)
        elif self.n1 > self.n2:
            ax.fill_between([xmin, 0], ymin, ymax, color='tab:gray', alpha=0.2)
        #ax.axhline(0, color='black', linewidth=0.5)
        #ax.axvline(0, color='black', linewidth=0.5)
        if self.s1 < 0:
            ax.plot([self.s1, self.s1], [0, y1], '-', color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        elif self.s1 > 0:
            ax.plot([self.s1, self.s1], [0, y1], '--', color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        if self.s2 > 0:
            ax.plot([self.s2, self.s2], [0, y2], '-', color='tab:orange', lw=3)  # Image height
            ax.annotate('', xy=(self.s2, y2), xytext=(self.s2, 0),
                        arrowprops=dict(color='tab:orange', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        elif self.s2 < 0:
            ax.plot([self.s2, self.s2], [0, y2], '--', color='tab:orange', lw=3)  # Image height
            ax.annotate('', xy=(self.s2, y2), xytext=(self.s2, 0),
                        arrowprops=dict(color='tab:orange', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))

        ax.plot([0, 0], [ymin, ymax], '-', color='black')  # Surface
        ax.plot([xmin, xmax], [0, 0], color='black', lw=1, linestyle=(0, (25, 5, 2, 5)))  # Optical axis

        ax.plot([self.f1, self.f1], [ymin, ymax], linestyle=(0, (8, 4)), color='tab:gray')  # Object focal plane
        ax.plot(self.f1, 0, 'o', color='tab:gray')
        ax.text(self.f1 + 0.5, 0.5, "F", color='tab:gray')
        ax.plot([self.f2, self.f2], [ymin, ymax], linestyle=(0, (8, 4)), color='tab:gray')  ## Image focal plane
        ax.plot(self.f2, 0, 'o', color='tab:gray')
        ax.text(self.f2 + 0.5, 0.5, "F'", color='tab:gray')
        ax.plot(self.r, 0, 'o', color='tab:red')
        ax.text(self.r + 0.5, 0.5, "C", color='tab:red')

        # Rays
        if self.s1 < 0:
            ax.plot([self.s1, 0], [y1, y1], '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.s1, y1, self.r, 0, self.s1, 0), '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.s1, y1, self.f1, 0, self.s1, 0), '-', color='black', lw=1)
        ax.plot(*line_interpolate(0, y1, self.f2, 0, 0, xmax), '-', color='black', lw=1)
        ax.plot(*line_interpolate(self.r, 0, self.s2, y2, 0, xmax), '-', color='black', lw=1)
        ax.plot([0, xmax], [y2, y2], '-', color='black', lw=1)
        if self.s2 < 0:
            ax.plot([self.s2, 0], [y2, y1], '--', color='black', lw=1)
            ax.plot([self.s2, 0], [y2, y2], '--', color='black', lw=1)
            ax.plot(*line_interpolate(self.s2, y2, self.r, 0, self.s2, 0), '--', color='black', lw=1)
        if self.s1 > 0:
            ax.plot([xmin, 0], [y1, y1], '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.f1, 0, self.s1, y1, xmin, 0), '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, xmin, 0), '-', color='black', lw=1)

            ax.plot([0, self.s1], [y1, y1], '--', color='black', lw=1)
            ax.plot(*line_interpolate(self.f1, 0, self.s1, y1, 0, self.s1), '--', color='black', lw=1)
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, 0, self.s1), '--', color='black', lw=1)

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        #print(min(y1, y2) - 10, max(y1, y2) + 10)
        plt.axis('off')
        fig.tight_layout()
        
        return fig
        #plt.show()

class SpheriView2:
    def __init__(self):
        pass

    def __new__(self, spheri_calc):
        self.spheri_calc = spheri_calc
        self.n1 = self.spheri_calc.n1
        self.n2 = self.spheri_calc.n2
        self.s1 = self.spheri_calc.s1
        self.s2 = self.spheri_calc.s2
        self.f1 = self.spheri_calc.f1
        self.f2 = self.spheri_calc.f2
        self.r = self.spheri_calc.r
        self.beta = self.spheri_calc.beta
        self.gamma = self.spheri_calc.gamma
        self.alpha = self.spheri_calc.alpha
        self.q1 = self.spheri_calc.q1
        self.q2 = self.spheri_calc.q2

        y0 = np.abs(self.r) * np.sin(np.radians(30))
        surf_y = np.linspace(-y0, y0, 100)
        surf_x = np.zeros_like(surf_y)
        if self.r > 0:
            surf_x = self.r - np.sqrt(self.r**2 - surf_y**2)
        elif self.r < 0:
            surf_x = self.r + np.sqrt(self.r**2 - surf_y**2)
        
        if np.abs(self.beta) < 1:
            y1 = y0 * 0.8
            y2 = self.beta * y1
        elif self.beta > 1:
            y2 = y0 * 0.8
            y1 = y2 / self.beta
        elif self.beta < -1:
            y2 = -y0 * 0.8
            y1 = y2 / self.beta
        
        # y1 = 10.0
        # y2 = self.beta * y1

        y_offset = max(y1, y2) * 0.3
        x_offset = max(abs(self.s1), abs(self.s2), abs(self.f1), abs(self.f2), 10) * 0.2
        ymin, ymax = min(y1, y2, 0) - y_offset, max(y1, y2, 0) + y_offset
        xmin, xmax = min(self.s1, self.s2, self.f1, self.f2, 0) - x_offset, max(self.s1, self.s2, self.f1, self.f2, 0) + x_offset

        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8, 3))
        ax.set_aspect('equal')
        # ax.grid()
        if self.n1 < self.n2:
            # ax.fill_between([0, xmax], ymin, ymax, color='tab:gray', alpha=0.2)
            ax.fill_betweenx(surf_y, surf_x, np.repeat(xmax, surf_y.shape), color='tab:gray', alpha=0.2)
        elif self.n1 > self.n2:
            # ax.fill_between([xmin, 0], ymin, ymax, color='tab:gray', alpha=0.2)
            ax.fill_betweenx(surf_y, np.repeat(xmin, surf_y.shape), surf_x, color='tab:gray', alpha=0.2)
        #ax.axhline(0, color='black', linewidth=0.5)
        #ax.axvline(0, color='black', linewidth=0.5)
        if self.s1 < 0:
            ax.plot([self.s1, self.s1], [0, y1], '-', color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
            #ax.arrow(self.s1, 0, 0, y1, width=1, length_includes_head=True, color='tab:blue')
        elif self.s1 > 0:
            ax.plot([self.s1, self.s1], [0, y1], '--', color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        if self.s2 > 0:
            ax.plot([self.s2, self.s2], [0, y2], '-', color='tab:orange', lw=3)  # Image height
            ax.annotate('', xy=(self.s2, y2), xytext=(self.s2, 0),
                        arrowprops=dict(color='tab:orange', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        elif self.s2 < 0:
            ax.plot([self.s2, self.s2], [0, y2], '--', color='tab:orange', lw=3)  # Image height
            ax.annotate('', xy=(self.s2, y2), xytext=(self.s2, 0),
                        arrowprops=dict(color='tab:orange', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        
        ax.plot([0, 0], [-y0, y0], linestyle=(0, (8, 4)), color='black')  # Surface
        ax.plot(surf_x, surf_y, '-', color='black')  # Surface2
        ax.plot([xmin, xmax], [0, 0], color='black', lw=1, linestyle=(0, (25, 5, 2, 5)))  # Optical axis

        ax.plot([self.f1, self.f1], [-y0, y0], linestyle=(0, (8, 4)), color='tab:gray')  # Object focal plane
        ax.plot(self.f1, 0, 'o', color='tab:gray')
        ax.text(self.f1 + (xmax-xmin)*0.005, (ymax-ymin)*0.04, "F", color='tab:gray')
        ax.plot([self.f2, self.f2], [-y0, y0], linestyle=(0, (8, 4)), color='tab:gray')  ## Image focal plane
        ax.plot(self.f2, 0, 'o', color='tab:gray')
        ax.text(self.f2 + (xmax-xmin)*0.005, (ymax-ymin)*0.04, "F'", color='tab:gray')
        ax.plot(self.r, 0, 'o', color='tab:red')
        ax.text(self.r + (xmax-xmin)*0.005, (ymax-ymin)*0.04, "C", color='tab:red')

        # Rays
        if self.s1 < 0:
            ax.plot([self.s1, 0], [y1, y1], '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.s1, y1, self.r, 0, self.s1, 0), '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.s1, y1, self.f1, 0, self.s1, 0), '-', color='black', lw=1)
        ax.plot(*line_interpolate(0, y1, self.f2, 0, 0, xmax), '-', color='black', lw=1)
        ax.plot(*line_interpolate(self.r, 0, self.s2, y2, 0, xmax), '-', color='black', lw=1)
        ax.plot([0, xmax], [y2, y2], '-', color='black', lw=1)
        if self.s2 < 0:
            ax.plot([self.s2, 0], [y2, y1], '--', color='black', lw=1)
            ax.plot([self.s2, 0], [y2, y2], '--', color='black', lw=1)
            ax.plot(*line_interpolate(self.s2, y2, self.r, 0, self.s2, 0), '--', color='black', lw=1)
        if self.s1 > 0:
            ax.plot([xmin, 0], [y1, y1], '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.f1, 0, self.s1, y1, xmin, 0), '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, xmin, 0), '-', color='black', lw=1)

            ax.plot([0, self.s1], [y1, y1], '--', color='black', lw=1)
            ax.plot(*line_interpolate(self.f1, 0, self.s1, y1, 0, self.s1), '--', color='black', lw=1)
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, 0, self.s1), '--', color='black', lw=1)

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(-y0, y0)
        #print(min(y1, y2) - 10, max(y1, y2) + 10)
        plt.axis('off')
        fig.tight_layout()
        #plt.show()

        return fig

if __name__ == "__main__":
    sph_calc01 = SpheriCalc(n1=1.33, n2=1.0, s1=-50, r=-30)
    sph_calc01 = SpheriCalc(n1=1.0, n2=1.5, s1=25, r=-10)
    fig1 = SpheriView2(sph_calc01)
    fig2 = SpheriView(sph_calc01)

    plt.show()
