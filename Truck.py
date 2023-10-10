# Creates a Truck object used to hold and deliver packages
class Truck:
    def __init__(self, id, time, distance=0):
        self.id = id
        self.packages = []
        self.distance = distance
        self.address = '4001 South 700 East'
        self.speed = 18
        self.time = time

    def __str__(self):
        return f"Truck ID: {self.id}, Packages: {self.packages}, Distance: {self.distance}, Time: {self.time}"

    # Increases the total distance the Truck object has traveled
    def increaseDistance(self, distance):
        self.distance += distance

    # Loads packages onto the Truck object
    def load_package(self, package):
        package.status = f"Loaded - Truck: {self.id}"
        self.packages.append(package)
        self.address = package.address




