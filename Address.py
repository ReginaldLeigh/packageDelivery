import csv


class Address:
    def __init__(self, id, location):
        self.id = id
        self.location = location

    def __str__(self):
        return f"Address ID: %s, Location: %s" % (self.id, self.location)
