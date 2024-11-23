import math

class RunwayComplex:
    def __init__(self, rw_NS=3 * math.pi / 2, rw_SN=math.pi / 2, rw_WE=0, rw_EW=math.pi):
        # Define runway angles in radians
        self.runways = {
            'NS': rw_NS,  # North-South runway angle (270°)
            'SN': rw_SN,  # South-North runway angle (90°)
            'WE': rw_WE,  # West-East runway angle (0°)
            'EW': rw_EW   # East-West runway angle (180°)
        }

    def calculate_wind_direction(self, wind_x, wind_y):
        # Check for no wind condition
        if wind_x == 0 and wind_y == 0:
            return None  # No wind condition

        # Use atan2, which handles all quadrants properly
        direction = math.atan2(wind_y, wind_x)
        
        # Normalize the result to be in the range [0, 2*pi]
        if direction < 0:
            direction += 2 * math.pi
        
        return direction


    def select_optimal_runway(self, wind_direction):
        if wind_direction is None:
            print("No wind detected. Defaulting to primary runway.")
            return 'NS'  # Default to North-South runway if no wind is present
        

        # Track the best runway
        optimal_runway = None
        best_headwind = -float('inf')  # We want to maximize the headwind
        lowest_crosswind = float('inf')  # We want to minimize the crosswind

        for runway, angle in self.runways.items():
            # Calculate the angular difference between the wind direction and runway direction
            angle_diff = (wind_direction - angle) % (2 * math.pi)
            if angle_diff > math.pi:  # Keep the difference within [-pi, pi]
                angle_diff -= 2 * math.pi

            # Compute headwind and crosswind components
            headwind = abs(math.cos(angle_diff))  # Along the runway
            crosswind = abs(math.sin(angle_diff))  # Perpendicular to the runway

            # Update the optimal runway if this runway has a better headwind
            # and a lower crosswind
            if headwind > best_headwind or (headwind == best_headwind and crosswind < lowest_crosswind):
                best_headwind = headwind
                lowest_crosswind = crosswind
                optimal_runway = runway

        return optimal_runway[1]+optimal_runway[0]

    def display_runway(self, runway):
        print(f"Activating LEDs for runway {runway}")
