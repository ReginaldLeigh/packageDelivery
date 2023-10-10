# Name: Reginald Leigh
# Student ID: 000485143

import datetime
from HashTable import *
from AddressList import *
from DistanceList import *
from Truck import *

# Create hash table and load package data
packages = HashTable()
packages.load_data('.\\Data Resources\\WGUPS Package File.csv')
print("Package Data Loaded")

# Create list of distances and load data
distance_list = DistanceList()
distance_list.load_data('.\\Data Resources\\DistanceTable.csv')
print("Distance Data Loaded")

# Create list of addresses and load data
address_list = AddressList()
address_list.load_data('.\\Data Resources\\Addresses.csv')
print("Address Data Loaded")

# Sets start time for each truck
t1start = datetime.timedelta(hours=8)
t2start = datetime.timedelta(hours=9, minutes=5)
t3start = datetime.timedelta(hours=11)

# List of package IDs that will be assigned to each truck
truck_loads = {
    'truck1': [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
    'truck2': [3, 6, 12, 17, 18, 21, 22, 23, 24, 25, 26, 27, 35, 36, 38, 39],
    'truck3': [2, 4, 5, 6, 7, 8, 9, 10, 11, 28, 32, 33]
}

# Sets the address for the hub
hubAddress = '4001 South 700 East'

# Initialize each Truck instance with their corresponding start times
truck1 = Truck(1, t1start)
truck2 = Truck(2, t2start)
truck3 = Truck(3, t3start)
truck_list = [truck1, truck2, truck3]


# Print all packages and current statuses
def printAllPackages():
    for package in packages.getallpackages():
        print(package)


# Uses two-dimension array (distance_list) to locate distance between two addresses
def distanceBetween(address1, address2):
    index_x = 0
    index_y = 0
    for row in address_list.table:  # Locate address in address list and assign ID to index
        if row.location == address1:
            index_y = row.id
        if row.location == address2:
            index_x = row.id
    return distance_list.table[index_y][index_x]  # Return distance


# Loops through list of packages and return package information for the nearest package
def minDistanceFrom(currentAddress, packageList):
    minDistance = 1000  # Initializes a high min distance for distance comparison
    minPackageId = 0
    minAddress = ''

    for package in packageList:  # Loops through packages and finds packages with the closest address
        id = package.id
        packageAddress = package.address
        distance = float(distanceBetween(currentAddress, packageAddress))
        if distance < minDistance:
            minDistance = distance
            minPackageId = id
            minAddress = packageAddress
    return [minPackageId, minAddress, minDistance]


# Loads packages onto trucks based on the truck_loads
def loadTrucks():
    for id in truck_loads['truck1']:
        package = packages.search(id)
        truck1.load_package(package)
    for id in truck_loads['truck2']:
        package = packages.search(id)
        truck2.load_package(package)
    for id in truck_loads['truck3']:
        package = packages.search(id)
        truck3.load_package(package)


# Cycles through Truck's packages and delivers items based on closest distance
# Process continues until stopTime is reached
def deliverPackages(truck, stopTime):
    if truck.time < stopTime:  # Gives current status if time period occurs before truck start time

        # Updates status at the start of the delivery route
        for package in truck.packages:
            package.status = f"En route - Truck: {truck.id}"

        while len(truck.packages) > 0:  # Delivers packages until stop time has been reached
            if truck.time < stopTime:

                # Returns info for closest package based on current address
                packageInfo = minDistanceFrom(truck.address, truck.packages)
                packageId = packageInfo[0]
                packageAddress = packageInfo[1]
                distance = packageInfo[2]

                deliveryTime = distance / truck.speed   # Calculates delivery time based on constant speed of 18mph
                truck.time = truck.time + datetime.timedelta(hours=deliveryTime)
                package = packages.search(packageId)
                package.status = f"Delivered {truck.time}, Truck: {truck.id}"
                truck.increaseDistance(distance)
                truck.address = packageAddress
                truck.packages.remove(package)
            else:
                return
    else:
        return

    # Returns truck back to hub once deliveries are complete
    returnDistance = float(
        distanceBetween(truck.address, hubAddress))
    returnTime = returnDistance / truck.speed
    truck.time = truck.time + datetime.timedelta(hours=returnTime)
    truck.increaseDistance(returnDistance)
    truck.address = hubAddress


# Display truck status based on distance and number of packages remaining
def status_message(truck):
    if truck.distance == 0:
        print(f"Truck {truck.id} is loaded at the hub, and has traveled {truck.distance} miles")
    elif len(truck.packages) > 0:
        print(f"Truck {truck.id} is currently en route, and has traveled {truck.distance} miles")
    else:
        print(f"Truck {truck.id} has finished its route, and has traveled {truck.distance} miles")


# Display introduction message to user in console
def console_intro():
    print("\n **** WGUPS Delivery Console **** \n")
    print("Which moment in time would you like to view?")
    print("Please enter all times in the form of HH:MM:SS as they would appear on a 24-hr clock")
    print("* IMPORTANT - All times start on or after 8AM (i.e. 08:00:00) *")


# Menu option which allows user to enter different periods in time
def time_entry():
    userInput = input("Time: ").split(":")
    try:
        time_instance = datetime.timedelta(hours=float(userInput[0]), minutes=float(userInput[1]),
                                           seconds=float(userInput[2]))
    except ValueError:
        print("Time instance may only contain valid numbers [0 - 9]")
        print("Please try again")
        return time_entry()

    # Clears truck information and prepares for new deliveries
    for truck in truck_list:
        truck.distance = 0
        truck.address = hubAddress
    truck1.time = t1start
    truck2.time = t2start
    truck3.time = t3start

    # Loads each truck and begins delivery process
    loadTrucks()
    deliverPackages(truck1, time_instance)
    deliverPackages(truck2, time_instance)

    # Used to ensure Truck3 does not leave until either Truck1 or Truck2 returns
    truck3.time = min(truck1.time, truck2.time)
    deliverPackages(truck3, time_instance)

    status_message(truck1)
    status_message(truck2)
    status_message(truck3)

    total_distance = truck1.distance + truck2.distance + truck3.distance

    print(f"Total distance traveled for all trucks is {total_distance} miles")
    return menu()  # Returns user to the main menu of the application


# Menu item which prints individual package information based on user input
def package_lookup():
    try:
        print("\nPlease enter a package ID to search, or enter '*' to exit")
        userInput = input("Package ID: ")
        if userInput == '*':
            return menu()
        else:
            packageID = int(userInput)
            package = packages.search(packageID)

            if package is None:
                print("The ID entered does not exist. Please try again.")
                return package_lookup()
            else:
                print(package)
                return menu()
    except ValueError:
        print("Please enter a valid number and try again.")
        return package_lookup()


# Main menu of the application
def menu():
    try:
        print("\nPlease select one of the following menu options:")
        print("""
            1 - Look Up Package ID
            2 - Print All Packages
            3 - Select New Time
            4 - Exit Program
            """)
        userSelect = int(input("Menu Option: "))
        if userSelect == 1:
            return package_lookup()
        if userSelect == 2:
            printAllPackages()
            return menu()
        if userSelect == 3:
            return time_entry()
        if userSelect == 4:
            exit()
        else:
            print("Please enter a valid menu option \n")
    except ValueError:
        print("Please enter a valid menu option \n")
        return menu()


# Starts the entire application
def main():
    console_intro()
    time_entry()
    menu()


main()
