import numpy as np


class OpticalSystem:
    def __init__(self, n0=1.0):
        self.n0 = n0  # Refractive index of the very left (first) medium
        self.components = []  # List to hold optical components
        self.components_pos = []  # List to hold positions of components
    
    def add_surf(self, surface, x):
        """Add an optical component to the system."""
        self.components.append(surface)
        self.components_pos.append(x)

    def f1(self):
        return - self.n1 * self.components[0].r / (self.n2 - self.n1)
    
    def f2(self):
        return self.n2 * self.components[0].r / (self.n2 - self.n1)
    
    def trace_image_1st_lens(self, object_x=0.0):
        comp1 = self.components[0]
        self.n2 = comp1.n2
        self.n1 = self.n0
        n1 = self.n1
        n2 = self.n2
        r = comp1.r
        self.s1 = object_x - self.components_pos[0]  # Object distance from the first surface
        self.s2 = n2 / ((n2 - n1) / r + n1 / self.s1)
        return self.s2
    
    def magnification(self):
        return (self.n1 / self.n2) * (self.s2 / self.s1)


class SpheriCalc:
    def __init__(self, *, n1=None, n2=None, s1=None, s2=None, r=None):
        self.values = {
            'n1': n1,
            'n2': n2,
            's1': s1,
            's2': s2,
            'r': r
        }

        # Ensure exactly one variable is missing
        missing = [k for k, v in self.values.items() if v is None]
        if len(missing) != 1:
            raise ValueError("Exactly one variable must be missing (set to None).")

        self.missing = missing[0]
        self._compute_missing()
        self._compute_other_values()

    def _compute_missing(self):
        n1 = self.values['n1']
        n2 = self.values['n2']
        s1 = self.values['s1']
        s2 = self.values['s2']
        r = self.values['r']

        m = self.missing

        # Compute the missing variable using rearranged equations
        if m == 'n1':
            if r == 'inf':
                self.values['n1'] = n2 * s1 / s2
            else:
                self.values['n1'] = (n2 * s1 * s2 - s1 * r * n2) / (s1 * s2 - r * s2)
        elif m == 'n2':
            if r == 'inf':
                self.values['n2'] = n1 * s2 / s1
            else:
                self.values['n2'] = (s2 * r * n1 - n1 * s1 * s2) / (s1 * r - s1 * s2)
        elif m == 's1':
            if r == 'inf':
                self.values['s1'] = n1 * s2 / n2
            else:
                self.values['s1'] = n1 * r * s2 / (n2 * r - (n2 - n1) * s2)
        elif m == 's2':
            if r == 'inf':
                self.values['s2'] = n2 * s1 / n1
            else:
                self.values['s2'] = n2 * r * s1 / ((n2 - n1) * s1 + n1 * r)
        elif m == 'r':
            if n1 == n2:
                raise ValueError("Cannot compute radius of curvature when n1 equals n2.")
            else:
                self.values['r'] = (n2 - n1) * s1 * s2 / (n2 * s1 - n1 * s2)
        
        self.n1 = self.values['n1']
        self.n2 = self.values['n2']
        self.s1 = self.values['s1']
        self.s2 = self.values['s2']
        self.r = self.values['r']

    def _compute_other_values(self):
        self.f1 = - (self.n1 * self.r) / (self.n2 - self.n1)  # Focal length before the surface
        self.f2 = (self.n2 * self.r) / (self.n2 - self.n1)  # Focal length after the surface
        self.beta = (self.n1 / self.n2) * (self.s2 / self.s1)  # Lateral magnification
        self.gamma = (self.n1 / self.n2) * (1 / self.beta)  # Angular magnification
        self.alpha = (self.n2 / self.n1) * self.beta**2  # Axial magnification
        self.q1 = self.s1 - self.f1  # Object distance before the surface
        self.q2 = self.s2 - self.f2  # Image distance after the surface

    def get(self, var_name):
        return self.values.get(var_name)

    def __repr__(self):
        return f"OpticalSystem({self.values})"


class SpheriCalc0:
    def __init__(self, r, n1, n2, s1):
        self.r = r  # Radius of curvature
        self.n1 = n1  # Refractive index of the medium before the surface
        self.n2 = n2  # Refractive indices of the media after the surface
        self.s1 = s1  # Object distance before the surface
        self.s2 = self.calc_s2(r, n1, n2, s1)  # Image distance

        self.beta1 = (self.n1 / self.n2) * (self.s2 / self.s1)  # Lateral magnification
        self.sigma1 = (self.n1 / self.n2) * (1 / self.beta1)  # Angular magnification

        self.f1 = self.calc_f1(r, n1, n2)  # Focal length before the surface
        self.f2 = self.calc_f2(r, n1, n2)  # Focal length after the surface

        self.q1 = self.s1 - self.f1  # Object distance before the surface
        self.q2 = self.s2 - self.f2  # Image distance after the surface

    def calc_s2(self, r, n1, n2, s1):
        return n2 / ((n2 - n1) / r + n1 / s1)

    def calc_f1(self, r, n1, n2):
        return - n1 * r / (n2 - n1)
    
    def calc_f2(self, r, n1, n2):
        return n2 * r / (n2 - n1)
    
    def plot(self, object_height=1.0):
        import matplotlib.pyplot as plt
        import numpy as np

        


class SphericalSurface:
    def __init__(self, n2, r):
        self.n2 = n2  # Refractive index of the medium after the surface
        self.r = r  # Radius of curvature of the surface


if __name__ == "__main__":
    # Example usage
    system = OpticalSystem()
    surface = SphericalSurface(n2=1.5, r=10.0)
    system.add_surf(surface, x=0.0)
    image_position = system.trace_image_1st_lens(object_x=-30.0)
    print(f"Image position: {image_position:.2f} mm from the surface")
    print(f"Magnification: {system.magnification():.2f}")
    f1 = system.f1()
    f2 = system.f2()
    print(f"f1: {f1:.2f}, f2: {f2:.2f}")

    sph_calc = SpheriCalc(n2=1.5, s1=-50, n1=1, r=30)
    print(sph_calc.q1)
    print(sph_calc.q2)
    print(sph_calc.f1)
    print(sph_calc.f2)
    print(sph_calc.beta)
    print(sph_calc.gamma)
    print(sph_calc.alpha)
    print(sph_calc)
