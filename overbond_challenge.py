import csv
import numpy as np
from scipy import interpolate

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


def yield_spread(corp, gov):
    # create two lists (term length, and bond names) with one pass
    benchmark_terms, benchmark_bonds = zip(*[(gov[g][0], g) for g in gov])
    yield_spread_dict = {}
    for bond in corp:
        i = (np.abs(np.array(benchmark_terms) - corp[bond][0])).argmin()
        benchmark = benchmark_bonds[i]
        spread = np.abs(corp[bond][1] - gov[benchmark][1])
        yield_spread_dict[bond] = [benchmark, round(spread, 2)]
    return yield_spread_dict


def spread_to_curve(corp, gov):
    gov_terms, gov_yields = zip(*[(gov[g][0], gov[g][1]) for g in gov])

    gov_curve = interpolate.interp1d(gov_terms, gov_yields)
    interpolated_yields = {}
    for c in corp:
        # corporate bond yield - interpolated yield of a government bond with the same term
        intp_yield = corp[c][1] - gov_curve(corp[c][0])
        interpolated_yields[c] = [round(intp_yield, 2)]
    return interpolated_yields

# helper function to write data to a csv
def write_data(data_dict, data_type, outfile):
    with open(outfile, 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        if data_type == "spread":
            csv_writer.writerow(("bond", "benchmark", "spread_to_benchmark"))
        elif data_type == "interpolated":
            csv_writer.writerow(("bond", "spread_to_curve"))
        for k, v in data_dict.items():
            csv_writer.writerow([k] + v)


if __name__ == "__main__":

    input_file = "sample_input.csv"
    corp, gov = read_data(input_file)

    spread = yield_spread(corp, gov)
    write_data(spread, "spread", "sample_yield.csv")

    intp = spread_to_curve(corp, gov)
    write_data(intp, "interpolated", "sample_intp_yield.csv")
