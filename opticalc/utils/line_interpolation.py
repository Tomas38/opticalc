import numpy as np


def demo_interpolate():
    print("Demo line interpolation")

def line_interpolate(x1, y1, x2, y2, X1, X2):
    """
    Calculate Y values for given X values on a line defined by two points.
    
    Parameters:
    x1, y1: coordinates of the first point defining the line
    x2, y2: coordinates of the second point defining the line
    X1, X2: x-coordinates for which to calculate corresponding y-coordinates
    
    Returns:
    Y1, Y2: y-coordinates corresponding to X1 and X2 on the defined line
    
    Raises:
    ValueError: if the two defining points have the same x-coordinate (vertical line)
    """
    
    # Check for vertical line (undefined slope)
    if x1 == x2:
        raise ValueError("Cannot define a line with two points having the same x-coordinate")
    
    # Calculate slope of the line
    slope = (y2 - y1) / (x2 - x1)
    
    # Calculate y-intercept using point-slope form: y - y1 = m(x - x1)
    # Rearranged to: y = mx - mx1 + y1
    y_intercept = y1 - slope * x1
    
    # Calculate Y1 and Y2 using the line equation: y = mx + b
    Y1 = slope * X1 + y_intercept
    Y2 = slope * X2 + y_intercept

    return np.array([[X1, X2], [Y1, Y2]])
    #return Y1, Y2
