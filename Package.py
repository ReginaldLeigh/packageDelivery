# Create a package object used to hold package data
class Package:
    def __init__(self, id, address, city, state, zip, deadline, mass, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.status = status

    def __str__(self):
        # object reference
        return f"Package ID: %s, Address: %s, City: %s, State: %s, Zip: %s, Deadline: %s, Mass: %s, Status: %s" \
            % (self.id, self.address, self.city, self.state, self.zip, self.deadline, self.mass, self.status)