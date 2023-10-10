import csv
from Address import *

class AddressList:
    def __init__(self):
        self.table = []

    def load_data(self, filename):
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            csvFile = csv.DictReader(file)
            for row in csvFile:
                id = int(row['id'])
                location = row['location']
                address = Address(id, location)
                self.table.append(address)

    def search(self, id):
        for address in self.table:
            if address.id == id:
                return address.location




