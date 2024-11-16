import queue
from wind_calculations import Wind
import random
class planes_queue:
    def __init__(self):
        self.planes = [] #our queue

    #Adding our planes to our queue
    def add_plane(self, plane_count):
        for i in range(plane_count):
            plane_name = f"plane{i+1}" #labeling each plane created
            x,y = random.uniform(-5,5), random.uniform(-5,5) #our wind velocity
            wind = Wind(x,y) #wind object consisting of direction and speed
            plane_data = {plane_name: wind} #Creating our dictionary
            self.planes.append(plane_data)

    #Check to see if we have any incoming planes in the queue
    def check_incoming_planes(self):
        if self.planes:
            current_p = self.planes.pop(0)
            print(f"Our current plane {current_p}")
        else:
            return None
        return current_p