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

        try:
            for k in self.values:
                # Convert +-inf and inf strings to np.inf
                if self.values[k] == np.inf or self.values[k] == 'inf' or self.values[k] == '+inf':
                    self.values[k] = np.inf
                elif self.values[k] == -np.inf or self.values[k] == '-inf':
                    self.values[k] = np.inf
                # Convert values to float if not None
                elif self.values[k] != None:
                    self.values[k] = float(self.values[k])
        except:
            raise ValueError("All input values must be numeric or None.")

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
            elif r == np.inf:
                self.values['n1'] = n2 * s1 / s2
            elif s1 == np.inf:
                self.values['n1'] = n2 - (n2 * r) / s2
            elif s2 == np.inf:
                self.values['n1'] = (n2 * s1) / (-r + s1)
            elif s1 == 0 or s2 == 0:
                raise ValueError("Cannot compute n1 when s1 or s2 are zero.")
            elif s1 == np.inf and s2 == np.inf:
                self.values['n1'] = n2
            elif s1 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n1 when both s1 and r are infinite.")
            elif s2 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n1 when both s2 and r are infinite.")
            elif s1 == r:
                raise ValueError("Cannot compute n1 when s1 equals r.")
            elif s2 == r:
                raise ValueError("Cannot compute n1 when s2 equals r.")
            else:
                self.values['n1'] = (n2 * s1 * s2 - s1 * r * n2) / (s1 * s2 - r * s2)
        elif m == 'n2':
            print(s1)
            if n1 < 1.0:
                raise ValueError("n1 must be greater than or equal to 1.0.")
            elif r == np.inf:
                self.values['n2'] = n1 * s2 / s1
            elif s1 == np.inf:
                print('here')
                self.values['n2'] = n1 * s2 / (-r + s2)
            elif s2 == np.inf:
                self.values['n2'] = n1 - (n1 * r) / s1
            elif s1 == 0 or s2 == 0:
                raise ValueError("Cannot compute n2 when s1 or s2 are zero.")
            elif s1 == np.inf and s2 == np.inf:
                self.values['n2'] = n1
            elif s1 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n2 when both s1 and r are infinite.")
            elif s2 == np.inf and r == np.inf:
                raise ValueError("Cannot compute n2 when both s2 and r are infinite.")
            elif s1 == r:
                raise ValueError("Cannot compute n2 when s1 equals r.")
            elif s2 == r:
                raise ValueError("Cannot compute n2 when s2 equals r.")
            else:
                print('there2')
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
                self.values['s2'] = n2 * r * s1 / ((n2 - n1) * s1 + n1 * r)
        elif m == 'r':
            if n1 < 1.0 or n2 < 1.0:
                raise ValueError("n must be greater than or equal to 1.0.")
            elif n1 == n2:
                raise ValueError("Cannot compute r when n1 equals n2.")
            elif s1 == 0.0 or s2 == 0.0:
                raise ValueError("Cannot compute r when s1 or s2 are zero.")
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
        
        if self.s1 != np.inf and self.s2 != np.inf:
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

# Example usage
if __name__ == "__main__":
    sph_calc01 = SpheriCalc(n1=1.5, n2=1.0, s1=-50, r=10)
    print(sph_calc01)
