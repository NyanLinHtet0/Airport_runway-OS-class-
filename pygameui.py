import pygame
import random
import math
from runway import RunwayComplex
from wind_calculations import Wind
from planes_queue import planes_queue

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Runway Selection with Dynamic Wind Updates")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Runway rectangles for visualization
runway_rects = {
    'NS': pygame.Rect(275, 50, 50, 500),  # North-South
    'SN': pygame.Rect(275, 50, 50, 500),  # South-North (same as N-S)
    'WE': pygame.Rect(50, 275, 500, 50),  # West-East
    'EW': pygame.Rect(50, 275, 500, 50)   # East-West (same as W-E)
}

# Initialize the RunwayComplex and Wind objects
airport = RunwayComplex()
wind = Wind()

# Initialize the plane queue and add planes to it
plane_queue = planes_queue()
plane_queue.add_plane(10)  # Add ten planes to the queue on startup

# Function to draw a wind direction arrow on the screen
def draw_wind_arrow(screen, start_pos, wind_x, wind_y):
    scale = 30  # Scale factor for arrow length
    end_pos = (start_pos[0] + wind_x * scale, start_pos[1] - wind_y * scale)

    # Draw main arrow line
    pygame.draw.line(screen, RED, start_pos, end_pos, 3)

    # Draw arrowhead
    angle = math.atan2(wind_y, wind_x)
    arrowhead_length = 10
    arrowhead_angle = math.pi / 6

    left_wing = (
        end_pos[0] - arrowhead_length * math.cos(angle + arrowhead_angle),
        end_pos[1] + arrowhead_length * math.sin(angle + arrowhead_angle)
    )
    right_wing = (
        end_pos[0] - arrowhead_length * math.cos(angle - arrowhead_angle),
        end_pos[1] + arrowhead_length * math.sin(angle - arrowhead_angle)
    )

    pygame.draw.line(screen, RED, end_pos, left_wing, 3)
    pygame.draw.line(screen, RED, end_pos, right_wing, 3)

# Main simulation loop with space-triggered updates
running = True
process_next_plane = False  # Flag to process the next plane only when space is pressed
font = pygame.font.SysFont(None, 24)

# Variables to store the current plane and wind info
current_plane_text = None
global_wind_text = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                process_next_plane = True  # Set flag to process the next plane

    # Clear the screen to white
    screen.fill(WHITE)

    # Draw runways
    for runway_label, rect in runway_rects.items():
        pygame.draw.rect(screen, GRAY, rect)

    # Process the next plane in the queue only when the space bar is pressed
    if process_next_plane:
        current_plane_data = plane_queue.check_incoming_planes()
        if current_plane_data:
            process_next_plane = False  # Reset flag

            # Get plane name and its associated wind object
            plane_name = list(current_plane_data.keys())[0]
            plane_wind: Wind = current_plane_data[plane_name]

            # Update global wind dynamically for this plane (new random values)
            new_wind_x = plane_wind.wind_x
            new_wind_y = plane_wind.wind_y
            wind.update_wind(new_wind_x, new_wind_y)  # Update global wind object

            # Calculate optimal runway based on global wind
            global_wind_direction = airport.calculate_wind_direction(new_wind_x, new_wind_y)
            assigned_runway_for_plane = airport.select_optimal_runway(global_wind_direction)

            # Generate text for display
            global_wind_text = f"Global Wind: ({new_wind_x:.2f}, {new_wind_y:.2f})"
            current_plane_text = f"Plane {plane_name}: Assigned Runway {assigned_runway_for_plane}"

            print(global_wind_text)
            print(current_plane_text)
        else:
            current_plane_text = "No incoming planes in queue."
            global_wind_text = None

    # Draw global wind info
    if global_wind_text:
        global_wind_surface = font.render(global_wind_text, True, BLACK)
        screen.blit(global_wind_surface, (10, 10))

    # Draw current plane info
    if current_plane_text:
        plane_surface = font.render(current_plane_text, True, BLACK)
        screen.blit(plane_surface, (10, 40))

    # Draw wind direction arrow
    if wind.wind_x != 0 or wind.wind_y != 0:
        normalized_x = wind.wind_x / max(abs(wind.wind_x), abs(wind.wind_y))
        normalized_y = wind.wind_y / max(abs(wind.wind_x), abs(wind.wind_y))
        draw_wind_arrow(screen, (300, 300), normalized_x, normalized_y)

    # Display "Press SPACE to process the next plane" message
    instruction_text = font.render("Press SPACE to process the next plane.", True, BLACK)
    screen.blit(instruction_text, (10, 550))

    # Update display with new frame data
    pygame.display.flip()

# Quit pygame when simulation ends
pygame.quit()
