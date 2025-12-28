import numpy as np
import matplotlib.pyplot as plt
from .utils import line_interpolate


class SpheriCalc:
    def __init__(self, *, n1, n2, s1, s2, r):
        # Original idea: (self, *, n1=None, n2=None, s1=None, s2=None, r=None)
        # But to avoid confusion, force user to always specify all except one variable
        # Also Pylace gave many red warnings with default None values...
        self.values = {
            'n1': n1,
            'n2': n2,
            's1': s1,
            's2': s2,
            'r': r
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
        self._compute_missing()

        # if self.s1 == np.inf or self.s2 == np.inf:
        #     self.type = 'afocal'
        # else:
        #     self.type = 'focal'

        self._compute_other_values()

    def _compute_missing(self):
        n1 = self.values['n1']
        n2 = self.values['n2']
        s1 = self.values['s1']
        s2 = self.values['s2']
        r = self.values['r']

        m = self.missing

        if n1 == np.inf or n2 == np.inf:
            raise ValueError("Refractive indices n1 and n2 must be finite values.")

        # Compute the missing variable using rearranged equations
        if m == 'n1':
            if n2 < 1.0:
                raise ValueError("n2 must be greater than or equal to 1.0.")
            elif s1 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n1 when both s1 and r are infinite.")
            elif s2 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n1 when both s2 and r are infinite.")
            elif r == np.inf:
                self.values['n1'] = n2 * s1 / s2
            elif s1 == np.inf:
                self.values['n1'] = n2 - (n2 * r) / s2
            elif s2 == np.inf:
                self.values['n1'] = (n2 * s1) / (-r + s1)
            elif s1 == 0 or s2 == 0:
                raise ValueError("Cannot compute n1 when s1 or s2 are zero.")
            elif s1 == r:
                raise ValueError("Cannot compute n1 when s1 equals r.")
            elif s2 == r:
                raise ValueError("Cannot compute n1 when s2 equals r.")
            elif s1 == np.inf and s2 == np.inf:
                self.values['n1'] = n2
            else:
                self.values['n1'] = (n2 * s1 * s2 - s1 * r * n2) / (s1 * s2 - r * s2)
        elif m == 'n2':
            if n1 < 1.0:
                raise ValueError("n1 must be greater than or equal to 1.0.")
            elif s1 == np.inf and s2 == np.inf:
                self.values['n2'] = n1
            elif s1 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n2 when both s1 and r are infinite.")
            elif s2 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n2 when both s2 and r are infinite.")
            elif r == np.inf:
                self.values['n2'] = n1 * s2 / s1
            elif s1 == np.inf:
                self.values['n2'] = n1 * s2 / (-r + s2)
            elif s2 == np.inf:
                self.values['n2'] = n1 - (n1 * r) / s1
            elif s1 == 0 or s2 == 0:
                raise ValueError("Cannot compute n2 when s1 or s2 are zero.")
            elif s1 == r:
                raise ValueError("Cannot compute n2 when s1 equals r.")
            elif s2 == r:
                raise ValueError("Cannot compute n2 when s2 equals r.")
            else:
                self.values['n2'] = (s2 * r * n1 - n1 * s1 * s2) / (s1 * r - s1 * s2)
        elif m == 's1':
            if n1 < 1.0 or n2 < 1.0:
                raise ValueError("n must be greater than or equal to 1.0.")
            elif s2 == np.inf and r == np.inf:
                self.values['s1'] = np.inf
            elif s2 == np.inf and n1 == n2:
                self.values['s1'] = np.inf
            elif r == np.inf:
                self.values['s1'] = n1 * s2 / n2
            elif s2 == np.inf:
                self.values['s1'] = n1 * r / (n1 - n2)
            elif n2*r == (n2 - n1)*s2:
                self.values['s1'] = np.inf
            else:
                # Includes n1 == n2 case
                self.values['s1'] = n1 * r * s2 / (n2 * r - (n2 - n1) * s2)
        elif m == 's2':
            if n1 < 1.0 or n2 < 1.0:
                raise ValueError("n must be greater than or equal to 1.0.")
            elif s1 == np.inf and r == np.inf:
                self.values['s2'] = np.inf
            elif s1 == np.inf and n1 == n2:
                self.values['s2'] = np.inf
            elif r == np.inf:
                self.values['s2'] = n2 * s1 / n1
            elif s1 == np.inf:
                self.values['s2'] = n2 * r / (n2 - n1)
            elif n1*r == -(n2 - n1)*s1:
                self.values['s2'] = np.inf
            else:
                # Includes n1 == n2 case
                self.values['s2'] = n2 * r * s1 / ((n2 - n1) * s1 + n1 * r)
        elif m == 'r':
            if n1 < 1.0 or n2 < 1.0:
                raise ValueError("n must be greater than or equal to 1.0.")
            elif n1 == n2:
                raise ValueError("Cannot compute r when n1 equals n2.")
            elif s1 == 0.0 or s2 == 0.0:
                raise ValueError("Cannot compute r when s1 or s2 is zero.")
            elif s1 == np.inf and s2 == np.inf:
                self.values['r'] = np.inf
            elif s1 == np.inf and s2 != np.inf:
                self.values['r'] = (n2 - n1) * s2 / (n2)
            elif s1 != np.inf and s2 == np.inf:
                self.values['r'] = - (n2 - n1) * s1 / (n1)
            elif n2 * s1 == n1 * s2:
                self.values['r'] = np.inf
            else:
                self.values['r'] = (n2 - n1) * s1 * s2 / (n2 * s1 - n1 * s2)
        
        self.n1 = self.values['n1']
        self.n2 = self.values['n2']
        self.s1 = self.values['s1']
        self.s2 = self.values['s2']
        self.r = self.values['r']

    def _compute_other_values(self):
        # Cases of f1 and f2
        if self.r == np.inf:
            self.f1 = np.inf
            self.f2 = np.inf
        elif self.n1 == self.n2:
            self.f1 = np.inf
            self.f2 = np.inf
        else:
            self.f1 = - (self.n1 * self.r) / (self.n2 - self.n1)
            self.f2 = (self.n2 * self.r) / (self.n2 - self.n1)
        
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
        
        if self.s1 == 0.0 and self.s2 == 0.0:
            self.beta = 1.0  # Lateral magnification
            self.gamma = (self.n1 / self.n2) * (1 / self.beta)  # Angular magnification
            self.alpha = (self.n2 / self.n1) * self.beta**2  # Axial magnification
        elif self.r == 0.0:
            self.beta = 0.0  # Lateral magnification
            self.gamma = np.nan  # Angular magnification
            self.alpha = 0.0  # Axial magnification
        elif self.s1 != np.inf and self.s2 != np.inf:
            self.beta = (self.n1 / self.n2) * (self.s2 / self.s1)  # Lateral magnification
            self.gamma = (self.n1 / self.n2) * (1 / self.beta)  # Angular magnification
            self.alpha = (self.n2 / self.n1) * self.beta**2  # Axial magnification
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
        return (f"=== Spherical surface ===\n"
                f"n1:    {self.n1:{sp}.{pr}f}\n"
                f"n2:    {self.n2:{sp}.{pr}f}\n"
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

    def plot1(self,
              xlim=None,
              ylim=None,
              ax=None,
              object_height=None,
              fill_medium=True,
              surface_as_arc=True,
              aspect_equal=False):
        # Create new figure only if ax is not provided
        if ax is None:
            fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8, 3))
            # Turn off axes visibility
            ax.axis('off')
        else:
            fig = ax.get_figure()
        # ax.grid()
        if aspect_equal is True:
            ax.set_aspect('equal')

        # Drawing surface
        surf_height = np.abs(self.r) * np.sin(np.radians(45))
        surf_y = np.linspace(-surf_height, surf_height, 100)
        surf_x = np.zeros_like(surf_y)
        if surface_as_arc is True:
            if self.r > 0:
                surf_x = self.r - np.sqrt(self.r**2 - surf_y**2)
            elif self.r < 0:
                surf_x = self.r + np.sqrt(self.r**2 - surf_y**2)
            ax.plot(surf_x, surf_y, '-', color='black')  # Surface as arc

        # Determine object and image heights
        if object_height is None:
            y1 = 0.5 * surf_height
        else:
            y1 = object_height
        y2 = self.beta * y1
        if self.s2 == np.inf:
            y2 = 0.0
        if self.s1 == np.inf:
            y2 = 10.0
            y1 = 0.0

        # Set window limits with some offsets
        y_offset = max(abs(y1), abs(y2)) * 0.3
        ymin = min(y1, y2, 0) - y_offset
        ymax = max(y1, y2, 0) + y_offset

        xmin = 0.0
        xmax = 0.0
        if self.s1 == np.inf:
            x_offset = max(abs(self.s2), abs(self.f1), abs(self.f2), 10) * 0.2
            xmin = min(self.s2, self.f1, self.f2, 0) - x_offset
            xmax = max(self.s2, self.f1, self.f2, 0) + x_offset
        elif self.s2 == np.inf:
            x_offset = max(abs(self.s1), abs(self.f1), abs(self.f2), 10) * 0.2
            xmin = min(self.s1, self.f1, self.f2, 0) - x_offset
            xmax = max(self.s1, self.f1, self.f2, 0) + x_offset
        else:
            x_offset = max(abs(self.s1), abs(self.s2), abs(self.f1), abs(self.f2), 10) * 0.2
            xmin = min(self.s1, self.s2, self.f1, self.f2, 0) - x_offset
            xmax = max(self.s1, self.s2, self.f1, self.f2, 0) + x_offset

        # Fix to have optical axis in the middle
        ylim_val = max(abs(ymin), abs(ymax))
        ymax = ylim_val
        ymin = -ylim_val

        # Override with user-defined limits
        if xlim is not None:
            xmin = xlim[0]
            xmax = xlim[1]
        if ylim is not None:
            ymin = ylim[0]
            ymax = ylim[1]

        # Shadding optical medium with higher refractive index
        if fill_medium is True:
            if surface_as_arc is False:
                if self.n1 < self.n2:
                    ax.fill_between([0, xmax], ymin, ymax, color='tab:gray', alpha=0.2)
                elif self.n1 > self.n2:
                    ax.fill_between([xmin, 0], ymin, ymax, color='tab:gray', alpha=0.2)
                elif self.n1 == self.n2:
                    pass  # No shading needed
            elif surface_as_arc is True:
                if self.n1 < self.n2:
                    # ax.fill_between([0, xmax], ymin, ymax, color='tab:gray', alpha=0.2)
                    ax.fill_betweenx(surf_y, surf_x, np.repeat(xmax, surf_y.shape), color='tab:gray', alpha=0.2)
                elif self.n1 > self.n2:
                    # ax.fill_between([xmin, 0], ymin, ymax, color='tab:gray', alpha=0.2)
                    ax.fill_betweenx(surf_y, np.repeat(xmin, surf_y.shape), surf_x, color='tab:gray', alpha=0.2)
                elif self.n1 == self.n2:
                    pass  # No shading needed

        # Drawing main plane H = H'
        ax.plot([0, 0], [ymin, ymax], linestyle=(0, (8, 4)), color='black')

        # Drawing optical axis
        ax.plot([xmin, xmax], [0, 0], color='black', lw=1, linestyle=(0, (25, 5, 2, 5)))  # Optical axis

        # Drawing focal planes
        if self.f1 != np.inf:
            ax.plot([self.f1, self.f1], [ymin, ymax], linestyle=(0, (8, 4)), color='tab:gray')  # Object focal plane
        if self.f2 != np.inf:
            ax.plot([self.f2, self.f2], [ymin, ymax], linestyle=(0, (8, 4)), color='tab:gray')  ## Image focal plane

        # Drawing object
        if self.s1 == np.inf:
            pass # No object to draw
        elif self.s1 < 0:
            # Real object
            ax.plot([self.s1, self.s1], [0, y1], '-', color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        elif self.s1 >= 0:
            # Virtual object
            ax.plot([self.s1, self.s1], [0, y1], linestyle=(0, (1, 1)), color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        
        # Drawing image
        if self.s2 == np.inf:
            pass  # No image to draw
        elif self.s2 > 0:
            # Real image
            ax.plot([self.s2, self.s2], [0, y2], '-', color='tab:orange', lw=3)  # Image height
            ax.annotate('', xy=(self.s2, y2), xytext=(self.s2, 0),
                        arrowprops=dict(color='tab:orange', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
        elif self.s2 <= 0:
            # Virtual image
            ax.plot([self.s2, self.s2], [0, y2], linestyle=(0, (1, 1)), color='tab:orange', lw=3)  # Image height
            ax.annotate('', xy=(self.s2, y2), xytext=(self.s2, 0),
                        arrowprops=dict(color='tab:orange', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))

        # Drawing rays
        if self.s1 < 0 and self.s1 != np.inf and self.s2 != np.inf:
            # Real object:
            # SOLID lines from object (x<0) to the surface (x=0)
            ax.plot([self.s1, 0], [y1, y1], '-', color='black', lw=1) if self.s1 != 0 else None
            ax.plot(*line_interpolate(self.s1, y1, self.r, 0, self.s1, 0), '-', color='black', lw=1) if self.s1 != self.r else None
            ax.plot(*line_interpolate(self.s1, y1, self.f1, 0, self.s1, 0), '-', color='black', lw=1) if self.s1 != self.f1 else None
        if self.s1 != np.inf and self.s2 != np.inf:
            # SOLID lines from surface to right side (x=xmax)
            ax.plot(*line_interpolate(0, y1, self.f2, 0, 0, xmax), '-', color='black', lw=1) if self.f2 != 0 else None
            ax.plot(*line_interpolate(self.r, 0, self.s2, y2, 0, xmax), '-', color='black', lw=1) if self.s2 != self.r else None
            ax.plot([0, xmax], [y2, y2], '-', color='black', lw=1)
        if self.s2 < 0 and self.s2 != np.inf:
            # Virtual image:
            # DASHED lines from surface (x=0) to image (x<0)
            ax.plot([self.s2, 0], [y2, y1], '--', color='black', lw=1) if self.s2 != 0 else None
            ax.plot([self.s2, 0], [y2, y2], '--', color='black', lw=1) if self.s2 != 0 else None
            ax.plot(*line_interpolate(self.s2, y2, self.r, 0, self.s2, 0), '--', color='black', lw=1) if self.s2 != self.r else None
        if self.s1 > 0 and self.s1 != np.inf:
            # Virtual object:
            # SOLID lines from the left (x=xmin) to the surface (x=0)
            ax.plot([xmin, 0], [y1, y1], '-', color='black', lw=1)
            ax.plot(*line_interpolate(self.f1, 0, self.s1, y1, xmin, 0), '-', color='black', lw=1) if self.s1 != self.f1 else None
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, xmin, 0), '-', color='black', lw=1) if self.s1 != self.r else None
            # DASHED lines from surface (x=0) to object (x>0)
            ax.plot([0, self.s1], [y1, y1], '--', color='black', lw=1) if self.s1 != 0 else None
            ax.plot(*line_interpolate(self.f1, 0, self.s1, y1, 0, self.s1), '--', color='black', lw=1) if self.s1 != self.f1 else None
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, 0, self.s1), '--', color='black', lw=1) if self.s1 != self.r else None
        if self.s1 == np.inf:
            ax.plot([0, self.s2], [y2, y2], '-', color='black', lw=1)
            ax.plot(*line_interpolate(0, y2, self.f1, 0, xmin, 0), '-', color='black', lw=1) if self.f1 != 0 else None
            ax.plot(*line_interpolate(self.r, 0, self.s2, y2, self.s2, 0), '-', color='black', lw=1) if self.s2 != self.r else None
            ax.plot(*line_interpolate(self.r, 0, self.s2, y2, xmin, 0), '-', color='black', lw=1) if self.s2 != self.r else None
        if self.s2 == np.inf:
            ax.plot([self.s1, 0], [y1, y1], '-', color='black', lw=1)
            ax.plot(*line_interpolate(0, y1, self.f2, 0, 0, xmax), '-', color='black', lw=1) if self.f2 != 0 else None
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, self.s1, 0), '-', color='black', lw=1) if self.s1 != self.r else None
            ax.plot(*line_interpolate(self.r, 0, self.s1, y1, 0, xmax), '-', color='black', lw=1) if self.s1 != self.r else None

        # Drawing points
        if self.f1 != np.inf and self.f1 > xmin and self.f1 < xmax:
            ax.plot(self.f1, 0, 'o', color='tab:gray')  # Object focal point
            ax.text(self.f1 + 0.5, 0.5, "F", color='tab:gray')  # Object focal point label
        if self.f2 != np.inf and self.f2 < xmax and self.f2 > xmin:
            ax.plot(self.f2, 0, 'o', color='tab:gray')  # Image focal point
            ax.text(self.f2 + 0.5, 0.5, "F'", color='tab:gray')  # Image focal point label
        ax.plot(self.r, 0, 'o', color='tab:red')  # Center of curvature
        ax.text(self.r + 0.5, 0.5, "C", color='tab:red')  # Center of curvature label

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        #print(min(y1, y2) - 10, max(y1, y2) + 10)
        #ax.axis('off')
        #fig.tight_layout()
        
        return fig
    
    def plot2(self):
        y0 = np.abs(self.r) * np.sin(np.radians(30))
        surf_y = np.linspace(-y0, y0, 100)
        surf_x = np.zeros_like(surf_y)
        if self.r > 0:
            surf_x = self.r - np.sqrt(self.r**2 - surf_y**2)
        elif self.r < 0:
            surf_x = self.r + np.sqrt(self.r**2 - surf_y**2)
        
        # Provide safe defaults so y1/y2 are always defined, then adjust based on beta
        y1 = 10.0
        y2 = self.beta * y1
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
        elif self.n1 == self.n2:
            pass  # No shading needed
        #ax.axhline(0, color='black', linewidth=0.5)
        #ax.axvline(0, color='black', linewidth=0.5)
        if self.s1 < 0:
            ax.plot([self.s1, self.s1], [0, y1], '-', color='tab:blue', lw=3)  # Object height
            ax.annotate('', xy=(self.s1, y1), xytext=(self.s1, 0),
                        arrowprops=dict(color='tab:blue', lw=0, shrinkA=0, shrinkB=-2,
                                        width=0, headwidth=10, headlength=12))
            #ax.arrow(self.s1, 0, 0, y1, width=1, length_includes_head=True, color='tab:blue')
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
