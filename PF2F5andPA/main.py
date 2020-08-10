import csv
import pprint

def parse_csv(file):
    #parse CSV into understandable components
    rules = []

    #open hosts file and read headers
    with open(file, 'rt') as file:
        rows = csv.reader(file)
        headers = next(rows)
        for row in rows:
            rules.append(row)
    return rules

file = 'ExampleInput.csv'

#def print_F5_Ouput

output = parse_csv(file)
print(output)