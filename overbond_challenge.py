import csv
import numpy as np

# reads data from the specified csv
# returns a dictionary {bond:[attributes]}
# assumes a well formed input - no error checking done on the csv
def read_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader, None) # to skip the header
        corporate, government = {}, {}
        for row in reader:
            if row[1] == "corporate":
                # term and yield are cast to floats in the attribute list
                corporate[row[0]] = [float(row[2].split(" ")[0]), float(row[3].split("%")[0])]
            elif row[1] == "government":
                government[row[0]] = [float(row[2].split(" ")[0]), float(row[3].split("%")[0])]
        return corporate, government


def yield_spread(corp, gov, outfile):
    # create two lists (term length, and bond names) with one pass
    benchmark_terms, benchmark_bonds = zip(*[(gov[g][0], g) for g in gov])
    yield_spread_dict = {}
    for bond in corp:
        i = (np.abs(np.array(benchmark_terms) - corp[bond][0])).argmin()
        benchmark = benchmark_bonds[i]
        spread = np.abs(corp[bond][1] - gov[benchmark][1])
        yield_spread_dict[bond] = [benchmark, str(spread)+"%"]

    with open(outfile, 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(("bond", "benchmark", "spread_to_benchmark"))
        for k, v in yield_spread_dict.items():
            csv_writer.writerow([k] + v)


if __name__ == "__main__":

    input_file = "sample_input.csv"
    corp, gov = read_data(input_file)
    #print(corp, gov)
    yield_spread(corp, gov, "test_out.csv")
