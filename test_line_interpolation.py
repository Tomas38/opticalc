from opticalc.utils import line_interpolate


# Test case 1: Simple line through (0,0) and (1,1)
(X1, X2), (Y1, Y2) = line_interpolate(0, 0, 1, 1, 0.5, 2)
print("Line through (0,0) and (1,1):")
print(f"X=0.5 -> Y={Y1}, X=2 -> Y={Y2}")

# Test case 2: Line with negative slope
(X1, X2), (Y1, Y2) = line_interpolate(0, 10, 5, 0, 2, 3)
print("\nLine through (0,10) and (5,0):")
print(f"X=2 -> Y={Y1}, X=3 -> Y={Y2}")

# Test case 3: Horizontal line
(X1, X2), (Y1, Y2) = line_interpolate(1, 5, 4, 5, 2, 10)
print("\nHorizontal line through (1,5) and (4,5):")
print(f"X=2 -> Y={Y1}, X=10 -> Y={Y2}")

# Test case 4: Line with fractional coordinates
(X1, X2), (Y1, Y2) = line_interpolate(1.5, 2.3, 3.7, 6.1, 2.0, 4.0)
print("\nLine through (1.5,2.3) and (3.7,6.1):")
print(f"X=2.0 -> Y={Y1:.2f}, X=4.0 -> Y={Y2:.2f}")

# Test case 5:
(X1, X2), (Y1, Y2) = line_interpolate(1.0, 1.0, 3.0, 2.0, 0.0, 5.0)
print("\nLine through (1.0,1.0) and (3.0,2.0):")
print(f"X=0.0 -> Y={Y1:.2f}, X=5.0 -> Y={Y2:.2f}")
