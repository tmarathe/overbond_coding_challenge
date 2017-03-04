import csv
import numpy as np
from scipy import interpolate
import difflib

# reads data from the specified csv
# returns a dictionary of the form: { bond : [ term, yield ] }
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

# takes two dictionaries - corporate bonds and government bonds
# returns a dictionary of the form: { bond : [ benchmark, difference ] }
# 'bond' is a coporate bond
# 'benchmark' is the id of the government bond with nearest term to 'bond'
# 'difference' is the difference between the 'bond' yield and 'benchmark' yield
def yield_spread(corp, gov):
    # create two lists (term length, and bond names) with one pass
    benchmark_terms, benchmark_bonds = zip(*[(gov[g][0], g) for g in gov])
    yield_spread_dict = {}
    for bond in corp:
        i = (np.abs(np.array(benchmark_terms) - corp[bond][0])).argmin()
        benchmark = benchmark_bonds[i]
        difference = corp[bond][1] - gov[benchmark][1]
        yield_spread_dict[bond] = [benchmark, round(difference, 2)]
    return yield_spread_dict

# returns a dictionary of the form { bond : [spread] }
# 'bond' is a corporate bond, 'spread' is the spread to curve
# government bond curve is calculated using linear interpolation
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
        if data_type == "benchmark":
            csv_writer.writerow(("bond", "benchmark", "spread_to_benchmark"))
        elif data_type == "curve":
            csv_writer.writerow(("bond", "spread_to_curve"))
        for k, v in data_dict.items():
            csv_writer.writerow([k] + v)


if __name__ == "__main__":

    # NOTE: If you run this file, you will need to keep the folder required_files in the same directory
    # the test compare generated files to those in the folder (which were calculated manually)

    # Tests
    input_files = ["small_input.csv", "sample_input.csv"]
    for i in input_files:
        corp, gov = read_data(i)
        i_name = i.split("_")[0]
        spread = yield_spread(corp, gov)
        write_data(spread, "benchmark", "generated_files/" + i_name + "_yield.csv")

        intp = spread_to_curve(corp, gov)
        write_data(intp, "curve", "generated_files/" + i_name + "_intp_yield.csv")

    generated = ["generated_files/small_yield.csv", "generated_files/small_intp_yield.csv", \
                 "generated_files/sample_yield.csv", "generated_files/sample_intp_yield.csv"]

    required = ["required_files/small_yield_required.csv", "required_files/small_intp_yield_required.csv", \
                "required_files/sample_yield_required.csv", "required_files/sample_intp_yield_required.csv"]


    for g, r in zip(generated, required):
        test = open(g).readlines()
        correct = open(g).readlines()

        diff = difflib.unified_diff(test, correct)
        if "".join(diff) == "":
            print("test passed")
        else:
            print("test failed")
