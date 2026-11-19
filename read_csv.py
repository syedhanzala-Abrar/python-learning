
import csv

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    print("Column names:", reader.fieldnames)

    for row in reader:
        print(row)
