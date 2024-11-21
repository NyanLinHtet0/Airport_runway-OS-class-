import RPi.GPIO as GPIO
import time
import math  # Import math to handle radians

from wind_calculations import Wind

# Define the GPIO pins for the LEDs
LED_PINS = {
    "North": 17,  # Pin for North LED
    "East": 27,   # Pin for East LED
    "South": 22,  # Pin for South LED
    "West": 23    # Pin for West LED
}

def setup_gpio():
    """Set up the GPIO pins for the LEDs."""
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    for pin in LED_PINS.values():
        GPIO.setup(pin, GPIO.OUT)  # Set all LED pins as output
        GPIO.output(pin, GPIO.LOW)  # Turn off all LEDs initially

def get_landing_direction(wind_direction):
    """
    Determine the optimal landing direction based on wind direction in radians.
    Opposite wind direction: The optimal landing direction is calculated as wind_direction + math.pi to get the opposite of the wind's origin.
    Modulo operation: (wind_direction + math.pi) % (2 * math.pi) ensures that the shifted direction stays within the range of 0 to 2π (0 to 360°).
    Cardinal directions: The unit circle is divided into four quadrants:
        East: Between 0 and π/4, or 7π/4 to 2π.
        North: Between π/4 and 3π/4.
        West: Between 3π/4 and 5π/4.
        South: Between 5π/4 and 7π/4.
    
    Args:
    wind_direction (float): The wind direction in radians (0 to 2π).
    
    Returns:
    str: The best landing direction (North, East, South, West).
    """
    # Calculate the opposite direction for landing (since planes land into the wind)
    landing_direction = (wind_direction + math.pi) % (2 * math.pi)  # Shift by π to get opposite direction

    # Map the landing direction to the nearest cardinal direction based on unit circle
    if 0 <= landing_direction < math.pi / 4 or 7 * math.pi / 4 <= landing_direction < 2 * math.pi:
        return "East"   # Wind from the West, land East
    elif math.pi / 4 <= landing_direction < 3 * math.pi / 4:
        return "North"  # Wind from the South, land North
    elif 3 * math.pi / 4 <= landing_direction < 5 * math.pi / 4:
        return "West"   # Wind from the East, land West
    else:
        return "South"  # Wind from the North, land South

def control_led(landing_direction):
    """
    Control the LEDs based on the landing direction.
    
    Args:
    landing_direction (str): The landing direction (North, East, South, West).
    """
    # Turn off all LEDs first
    for direction, pin in LED_PINS.items():
        GPIO.output(pin, GPIO.LOW)
    
    # Light up the corresponding LED
    GPIO.output(LED_PINS[landing_direction], GPIO.HIGH)
    print(f"LED for {landing_direction} is ON.")

def cleanup_gpio():
    """Cleanup the GPIO settings before exiting."""
    GPIO.cleanup()

def assign_runway_to_planes(plane_queue, wind_direction, wind_speed):
    """
    Assign the optimal landing direction and wind speed to planes in the queue.
    
    Args:
    plane_queue (list): List of planes (by name or ID) waiting to land.
    wind_direction (float): The wind direction in radians (0 to 2π).
    wind_speed (float): The wind speed.
    
    Returns:
    dict: A dictionary where keys are plane IDs and values are tuples containing:
          (assigned landing direction, wind speed).
    """
    # Get the optimal landing direction based on wind direction
    landing_direction = get_landing_direction(wind_direction)
    
    # Dictionary to hold the planes and their assigned landing direction and wind speed
    assigned_info = {}
    
    # Loop through each plane in the queue
    for plane in plane_queue:
        # Assign the landing direction and wind speed to the plane
        assigned_info[plane] = (landing_direction, wind_speed)
        print(f"Plane {plane} assigned to land in direction: {landing_direction}, Wind Speed: {wind_speed:.2f}")
    
    return assigned_info


# Example usage of assign_runway_to_planes
if __name__ == "__main__":
    try:
        setup_gpio()
        wind_directions = float(input("Enter wind direction in radians (0 to 2π): "))
        plane_queue = ["Plane A", "Plane B", "Plane C"]  # Simulated plane queue
        assigned_runways = assign_runway_to_planes(plane_queue, wind_directions)
        print(f"Assigned landing directions: {assigned_runways}")
        
        # Light up LED based on the first plane's landing direction for demonstration
        first_plane_direction = assigned_runways[plane_queue[0]]
        control_led(first_plane_direction)
        
        # Keep the LED on for 5 seconds for visibility
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("Program interrupted.")
    except ValueError:
        print("Please enter a valid number for wind direction.")
    finally:
        cleanup_gpio()

# Assuming Wind class is imported from wind_calculations.py

if __name__ == "__main__":
    try:
        setup_gpio()

        # Example: Initialize wind with X and Y components
        wind = Wind(3, 4)  # Example values for wind_x and wind_y

        # Get the wind speed and wind direction in radians
        wind_speed = wind.calculate_wind_speed()
        wind_direction_radians = wind.calculate_wind_direction_radians()

        # Check if the wind speed is significant enough to calculate landing direction
        if wind_speed > 0 and wind_direction_radians is not None:
            print(f"Wind Speed: {wind_speed:.2f} units")
            print(f"Wind Direction (radians): {wind_direction_radians:.2f}")

            # Example plane queue
            plane_queue = ["Plane A", "Plane B", "Plane C"]

            # Assign runway directions and wind speed to each plane
            assigned_runways = assign_runway_to_planes(plane_queue, wind_direction_radians, wind_speed)
            print(f"Assigned landing directions and wind speeds: {assigned_runways}")

            # Control LED based on the first plane's landing direction
            first_plane_direction = assigned_runways[plane_queue[0]][0]  # Extract landing direction
            control_led(first_plane_direction)

            # Keep the LED on for 5 seconds for visibility
            time.sleep(5)
        else:
            print("No significant wind detected or unable to determine wind direction.")
        
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        cleanup_gpio()
