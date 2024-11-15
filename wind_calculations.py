class Wind:
    def __init__(self, wind_x=0, wind_y=0):
        #Initialize the Wind class with default or given wind vector components.
        self.wind_x = wind_x
        self.wind_y = wind_y

    def calculate_wind_speed(self):
        #Calculate the magnitude of wind speed using the Pythagorean theorem.
        return (self.wind_x**2 + self.wind_y**2) ** 0.5

    def calculate_wind_direction(self):
        #Calculate the wind direction in degrees (angle with respect to the X-axis).
        import math
        if self.wind_x == 0 and self.wind_y == 0:
            return None  # No direction if wind speed is zero
        return math.degrees(math.atan2(self.wind_y, self.wind_x))

    def update_wind(self, wind_x, wind_y):
        #Update the wind vector components.
        self.wind_x = wind_x
        self.wind_y = wind_y

    def display_info(self):
        #Display wind speed and direction information.
        speed = self.calculate_wind_speed()
        direction = self.calculate_wind_direction()
        print(f"Wind Speed: {speed:.2f} units")
        if direction is not None:
            print(f"Wind Direction: {direction:.2f}°")
        else:
            print("Wind Direction: Undefined (no wind)")

# wind = Wind(3, 4)
# wind.display_info()
# wind.update_wind(0, 0)
# wind.display_info()
