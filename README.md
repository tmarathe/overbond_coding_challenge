# Overbond Coding Challenge
## By Tarang Marathe

The file `overbond_challenge.py` contains all the functions required to solve the two exercises. Code is written in Python 3, and the required libraries are `csv` (to read and write .csv files), `numpy`, `scipy` (for various mathematical functions), and `difflib` for testing the generated files.

The function `read_data()` takes a filename/path of a source .csv file and and returns two Python dictionary whose keys are the unique bond ids (C1, G1, etc), and values are a list of attributes (term, yield) of the corresponding bond. This data structure was chosen because lookup from a hashtable/dictionary is amortized O(1). One of the dictionaries returned contains the information for corporate bonds, the other is for government bonds.

The function `yield_spread()` calculates the yield spread for each corporate bond by searching the dictionary of government bonds for the the one with the closest term to maturity, and computing the difference in yields. If the corporate bond dictionary has *m* entries the government bond dictionary has *n*, this operation has a worst-case of O(mn).

This could be improved - given more time - if we implemented a self-balancing binary tree data structure (AVL, Red-Black) that sorted bonds based on their term. In this case, searching for the government bond with nearest term for each corporate bond within the binary tree would have a worst-case of O(m log n). 

Similarly, the `spread_to_curve()` function calculates the spread to the government bond curve for each corporate bond. The government bond curve is calculated using the `scipy` function `interpolate.interp1d`. This curve can be used to find the interpolated yield value for the term of each corporate bond, and the difference of these terms is the required spread to curve.

Finally, the `write_data()` function takes a dictionary data structure computed by either `yield_spread()` or `spread_to_curve()` and writes the data to a .csv file.

Some tests have been included in the `__main__` scope. 

Note: If you run `overbond_challenge.py`, you will need to keep the folder `required_files` in the same directory, as the test compare generated files to those in the folder (which were calculated manually). Alternatively, you can comment out the tests and call the functions on files of your own, or import the functions into another test script to run.