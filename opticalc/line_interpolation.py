import numpy as np

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
    # return Y1, Y2


# Example usage and test cases
# if __name__ == "__main__":
#     # Test case 1: Simple line through (0,0) and (1,1)
#     Y1, Y2 = line_interpolate(0, 0, 1, 1, 0.5, 2)
#     print("Line through (0,0) and (1,1):")
#     print(f"X=0.5 -> Y={Y1}, X=2 -> Y={Y2}")
    
#     # Test case 2: Line with negative slope
#     Y1, Y2 = line_interpolate(0, 10, 5, 0, 2, 3)
#     print("\nLine through (0,10) and (5,0):")
#     print(f"X=2 -> Y={Y1}, X=3 -> Y={Y2}")
    
#     # Test case 3: Horizontal line
#     Y1, Y2 = line_interpolate(1, 5, 4, 5, 2, 10)
#     print("\nHorizontal line through (1,5) and (4,5):")
#     print(f"X=2 -> Y={Y1}, X=10 -> Y={Y2}")
    
#     # Test case 4: Line with fractional coordinates
#     Y1, Y2 = line_interpolate(1.5, 2.3, 3.7, 6.1, 2.0, 4.0)
#     print("\nLine through (1.5,2.3) and (3.7,6.1):")
#     print(f"X=2.0 -> Y={Y1:.2f}, X=4.0 -> Y={Y2:.2f}")

#       # Test case 5:
#     Y1, Y2 = line_interpolate(1.0, 1.0, 3.0, 2.0, 0.0, 5.0)
#     print("\nLine through (1.0,1.0) and (3.0,2.0):")
#     print(f"X=0.0 -> Y={Y1:.2f}, X=5.0 -> Y={Y2:.2f}")