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
