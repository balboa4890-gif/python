import math

def get_point(prompt):
    """Gets a 3D point from the user."""
    while True:
        try:
            raw_input = input(prompt)
            coords = [float(c.strip()) for c in raw_input.split(',')]
            if len(coords) != 3:
                print("Error: Please enter three coordinates (x, y, z).")
                continue
            return tuple(coords)
        except ValueError:
            print("Error: Invalid input. Please enter numbers separated by commas.")

def calculate_distance(p1, p2):
    """Calculates the Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def main():
    """Main function to run the distance calculator."""
    print("3D Distance Calculator")
    print("Enter the coordinates for each point as x, y, z")
    
    point1 = get_point("Enter coordinates for point 1 (e.g., 1, 2, 3): ")
    point2 = get_point("Enter coordinates for point 2 (e.g., 4, 5, 6): ")
    
    distance = calculate_distance(point1, point2)
    
    print(f"\nPoint 1: {point1}")
    print(f"Point 2: {point2}")
    print(f"Distance: {distance:.4f}")

if __name__ == '__main__':
    main()


