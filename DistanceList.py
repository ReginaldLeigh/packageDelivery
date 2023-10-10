import csv


class DistanceList:
    def __init__(self):
        self.table = []

    def load_data(self, filename):
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            csvFile = csv.reader(file)
            for row in csvFile:
                self.table.append(row)
