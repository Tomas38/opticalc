import numpy as np


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
            elif s1 == 'inf':
                self.values['n1'] = n2 - (n2 * r) / s2
            elif s2 == 'inf':
                self.values['n1'] = (n2 * s1) / (-r + s1)
            else:
                self.values['n1'] = (n2 * s1 * s2 - s1 * r * n2) / (s1 * s2 - r * s2)
        elif m == 'n2':
            print(s1)
            if r == 'inf':
                self.values['n2'] = n1 * s2 / s1
            elif s1 == 'inf':
                print('here')
                self.values['n2'] = n1 * s2 / (-r + s2)
            elif s2 == 'inf':
                self.values['n2'] = n1 - (n1 * r) / s1
            else:
                print('there2')
                self.values['n2'] = (s2 * r * n1 - n1 * s1 * s2) / (s1 * r - s1 * s2)
        elif m == 's1':
            if r == 'inf':
                self.values['s1'] = n1 * s2 / n2
            elif s2 == 'inf':
                self.values['s1'] = n1 * r / (n1 - n2)
            else:
                self.values['s1'] = n1 * r * s2 / (n2 * r - (n2 - n1) * s2)
        elif m == 's2':
            if r == 'inf':
                self.values['s2'] = n2 * s1 / n1
            elif s1 == 'inf':
                self.values['s2'] = n2 * r / (n2 - n1)
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
        if self.s1 != 'inf' and self.s2 != 'inf':
            self.beta = (self.n1 / self.n2) * (self.s2 / self.s1)  # Lateral magnification
            self.gamma = (self.n1 / self.n2) * (1 / self.beta)  # Angular magnification
            self.alpha = (self.n2 / self.n1) * self.beta**2  # Axial magnification
            self.q1 = self.s1 - self.f1  # Object distance before the surface
            self.q2 = self.s2 - self.f2  # Image distance after the surface

    def get(self, var_name):
        return self.values.get(var_name)

    def __repr__(self):
        return f"OpticalSystem({self.values})"
    
    def __str__(self):
        return (f"=== Spherical surface ===\n"
                f"n1:\t{self.n1:<.2f}\n"
                f"n2:\t{self.n2:<.2f}\n"
                f"s1:\t{self.s1}\n"
                f"s2:\t{self.s2}\n"
                f"r:\t{self.r:<.2f}\n"
                f"f1:\t{self.f1:<.2f}\n"
                f"f2:\t{self.f2:<.2f}\n"
                #f"beta:\t{self.beta}\n"
                #f"gamma:\t{self.gamma}\n"
                #f"alpha:\t{self.alpha}\n"
                #f"q1:\t{self.q1}\n"
                #f"q2:\t{self.q2}\n"
                f"=========================")
