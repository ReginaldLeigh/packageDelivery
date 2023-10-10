import csv
from Package import *

# Creates a hash table to store package data
class HashTable:
    def __init__(self, capacity=10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Inserts packages into hash table using the ID
    def insert(self, id, package):
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == id:
                kv[1] = package
                return True
        key_value = [id, package]
        bucket_list.append(key_value)
        return True

    # Uses package ID to find primary bucket and search all packages
    def search(self, id):
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if item[0] == id:
                return item[1]
        return None

    # Removes an item from the hash table
    def remove(self, id):
        bucket = hash(id) % len(self.table)
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if item[0] == id:
                bucket_list.remove([item[0], item[1]])

    # Load data from a CSV into the hash table
    def load_data(self, filename):
        with open(filename, mode='r') as file:
            csvFile = csv.DictReader(file)
            for row in csvFile:
                id = int(row['id'])
                address = row['address']
                city = row['city']
                state = row['state']
                zip = row['zip']
                deadline = row['deadline']
                mass = row['mass']
                status = "At Hub"

                package = Package(id, address, city, state, zip, deadline, mass, status)
                self.insert(package.id, package)

    # Returns a list of all packages within the hash table
    def getallpackages(self):
        packages = []
        for bucket in self.table:
            if bucket:
                for package in bucket:
                    packages.append(package[1])
        return packages

    # Prints all packages within the hash table
    def showallpackages(self):
        for bucket in self.table:
            if bucket:
                for package in bucket:
                    print(package[1])







