import RPi.GPIO as GPIO
import time

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

def get_landing_direction(wind_directions):
    """
    Determine the optimal landing direction based on wind direction.
    
    Args:
    wind_directions (float): The wind direction in degrees (0-360).
    
    Returns:
    str: The best landing direction (North, East, South, West).
    """
    wind_direction = wind_directions % 360

    if 45 <= wind_direction < 135:
        return "South"  # Wind coming from the East
    elif 135 <= wind_direction < 225:
        return "West"   # Wind coming from the South
    elif 225 <= wind_direction < 315:
        return "North"  # Wind coming from the West
    else:
        return "East"   # Wind coming from the North

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


def assign_runway_to_planes(plane_queue, wind_directions):
    """
    Assign the optimal landing direction to planes in the queue.
    
    Args:
    plane_queue (list): List of planes (by name or ID) waiting to land.
    wind_directions (float): The wind direction in degrees (0-360).
    
    Returns:
    dict: A dictionary where keys are plane IDs and values are the assigned landing directions.
    """
    # Get the optimal landing direction based on wind direction
    landing_direction = get_landing_direction(wind_directions)
    
    # Dictionary to hold the planes and their assigned landing direction
    assigned_directions = {}
    
    # Loop through each plane in the queue
    for plane in plane_queue:
        # Assign the landing direction to the plane
        assigned_directions[plane] = landing_direction
        print(f"Plane {plane} assigned to land in direction: {landing_direction}")
    
    return assigned_directions

# Example usage of assign_runway_to_planes
if __name__ == "__main__":
    try:
        setup_gpio()
        wind_directions = float(input("Enter wind direction in degrees (0-360): "))
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

# Example usage
if __name__ == "__main__":
    try:
        setup_gpio()
        wind_directions = float(input("Enter wind direction in degrees (0-360): "))
        landing_direction = get_landing_direction(wind_directions)
        print(f"The optimal landing direction is: {landing_direction}")
        control_led(landing_direction)
        
        # Keep the LED on for 5 seconds for visibility
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("Program interrupted.")
    except ValueError:
        print("Please enter a valid number for wind direction.")
    finally:
        cleanup_gpio()
