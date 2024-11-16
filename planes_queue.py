import queue
import threading
class planes_queue:
    def __init__(self):
        self.planes = [] #our queue

    #Adding our planes to our queue
    def add_plane(self, plane_count):
        for i in range(plane_count):
            my_current_plane = f"plane{i + 1}"
            self.planes.append(my_current_plane)

    #Check to see if we have any incoming planes in the queue
    def check_incoming_planes(self):
        while self.planes:
            current_p = self.planes.pop(0)
            print(f"Our current plane {current_p}")
            return current_p

