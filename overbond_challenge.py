import numpy as np
import csv

# reads data from the specified csv
# returns a dictionary {bond:[attributes]}
# assumes a well formed input - no error checking done on the csv
def read_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader, None) # to skip the header
        # term and yield are cast to floats in the attribute list
        bond_dict = {row[0]:[row[1], float(row[2].split(" ")[0]), \
                             float(row[3].split("%")[0])] for row in reader}
        print(bond_dict)



if __name__ == "__main__":

    input_file = "small_input.csv"
    read_data(input_file)
