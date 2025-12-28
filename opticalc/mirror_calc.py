import numpy as np
import matplotlib.pyplot as plt
from .utils import line_interpolate


class MirrorCalc:
    def __init__(self, *, s1, s2, r):
        self.values = {
            's1': s1,
            's2': s2,
            'r': r,
        }

        try:
            for k in self.values:
                # Convert +-inf and inf strings to np.inf
                if self.values[k] == np.inf or self.values[k] == 'inf' or self.values[k] == '+inf':
                    self.values[k] = np.inf
                elif self.values[k] == -np.inf or self.values[k] == '-inf':
                    self.values[k] = np.inf
                # Convert values to float if not None
                elif self.values[k] is not None:
                    self.values[k] = float(self.values[k])
        except Exception as e:
            raise ValueError("All input values must be numeric or None.") from e

        # Ensure exactly one variable is missing
        missing = [k for k, v in self.values.items() if v is None]
        if len(missing) != 1:
            raise ValueError("Exactly one variable must be missing (set to None).")

        self.missing = missing[0]
        s1 = self.values['s1']
        s2 = self.values['s2']
        r = self.values['r']

        m = self.missing

        # Compute the missing variable
        if m == 's1':
            if r == np.inf and s2 == np.inf:
                self.values['s1'] = np.inf
            elif r == np.inf:
                self.values['s1'] = -s2
            elif s2 == np.inf:
                self.values['s1'] = r / 2
            elif r == 2 * s2:
                self.values['s1'] = np.inf
            else:
                self.values['s1'] = (s2 * r) / (2 * s2 - r)
        elif m == 's2':
            if r == np.inf and s1 == np.inf:
                self.values['s2'] = np.inf
            elif r == np.inf:
                self.values['s2'] = -s1
            elif s1 == np.inf:
                self.values['s2'] = r / 2
            elif r == 2 * s1:
                self.values['s2'] = np.inf
            else:
                self.values['s2'] = (s1 * r) / (2 * s1 - r)
        elif m == 'r':
            if s1 == np.inf and s2 == np.inf:
                self.values['r'] = np.inf
            elif s1 == np.inf:
                self.values['r'] = 2 * s2
            elif s2 == np.inf:
                self.values['r'] = 2 * s1
            elif s1 == -s2:
                self.values['r'] = np.inf
            else:
                self.values['r'] = (2 * s1 * s2) / (s1 + s2)
        
        self.s1 = self.values['s1']
        self.s2 = self.values['s2']
        self.r = self.values['r']

        # Compute other related values
        # Cases of f1 and f2
        if self.r == np.inf:
            self.f1 = np.inf
            self.f2 = np.inf
        else:
            self.f1 = self.r / 2
            self.f2 = self.r / 2
        
        # Cases of q1 and q2
        if self.s1 == np.inf and self.s2 == np.inf:
            self.q1 = np.inf
            self.q2 = np.inf
        elif self.f1 == np.inf and self.f2 == np.inf:
            self.q1 = np.inf
            self.q2 = np.inf
        elif self.s1 == np.inf and self.s2 != np.inf:
            self.q1 = np.inf
            self.q2 = 0.0
        elif self.s2 == np.inf and self.s1 != np.inf:
            self.q1 = 0.0
            self.q2 = np.inf
        else:
            self.q1 = self.s1 - self.f1
            self.q2 = self.s2 - self.f2
        
        if self.s1 != np.inf and self.s2 != np.inf:
            self.beta = - (self.s2 / self.s1)  # Lateral magnification
            self.gamma = - (1 / self.beta)  # Angular magnification
            self.alpha = - self.beta**2  # Axial magnification
        elif self.s1 == np.inf and self.s2 != np.inf:
            self.beta = 0.0
            self.gamma = np.inf
            self.alpha = 0.0
        elif self.s1 != np.inf and self.s2 == np.inf:
            self.beta = np.inf
            self.gamma = 0.0
            self.alpha = np.inf
        #elif self.s1 == np.inf and self.s2 == np.inf:
        #    self.beta = 0.0
        #    self.gamma = np.inf
        #    self.alpha = 0.0
        else:
            self.beta = np.nan
            self.gamma = np.nan
            self.alpha = np.nan

    def get(self, var_name):
        return self.values.get(var_name)

    def __repr__(self):
        return f"OpticalSystem({self.values})"
    
    def __str__(self):
        # Spacing and precision
        sp = 18
        pr = 4
        return (f"=== Spherical mirror ===\n"
                f"s1:    {self.s1:{sp}.{pr}f}\n"
                f"s2:    {self.s2:{sp}.{pr}f}\n"
                f"r:     {self.r:{sp}.{pr}f}\n"
                f"f1:    {self.f1:{sp}.{pr}f}\n"
                f"f2:    {self.f2:{sp}.{pr}f}\n"
                f"beta:  {self.beta:{sp}.{pr}f}\n"
                f"gamma: {self.gamma:{sp}.{pr}f}\n"
                f"alpha: {self.alpha:{sp}.{pr}f}\n"
                f"q1:    {self.q1:{sp}.{pr}f}\n"
                f"q2:    {self.q2:{sp}.{pr}f}\n"
                f"=========================")

    def plot1(self):
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
        #ax.axhline(0, color='black', linewidth=0.5)
        #ax.axvline(0, color='black', linewidth=0.5)
        if self.s1 < 0:
            ax.plot([self.s1, self.s1], [0, y1], '-', color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        elif self.s1 > 0:
            ax.plot([self.s1, self.s1], [0, y1], linestyle=(0, (1, 1)), color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        if self.s2 > 0:
            ax.plot([self.s2, self.s2], [0, y2], '-', color='tab:orange', lw=3)  # Image height
            ax.annotate('', xy=(self.s2, y2), xytext=(self.s2, 0),
                        arrowprops=dict(color='tab:orange', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        elif self.s2 < 0:
            ax.plot([self.s2, self.s2], [0, y2], linestyle=(0, (1, 1)), color='tab:orange', lw=3)  # Image height
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
