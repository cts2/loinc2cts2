import csv


class LoincReader:
    def __init__(self, csv_path):
        self.data = []
        self.csv_path = csv_path

    def read(self, row_callback):
        with open(self.csv_path, 'rb') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            for row in csvreader:
                row_callback(row)
