
from datetime import datetime


class RideRequest:

    def __init__(self, name, destination, time_slot, year):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.submitted_at = datetime.now()


class Cab:

    def __init__(self, driver, seats, destination, time_slot):
        self.driver = driver
        self.seats = seats
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.passengers = []
