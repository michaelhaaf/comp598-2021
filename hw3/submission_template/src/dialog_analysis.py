#!/usr/bin/env python3

import pandas as pd
import json
import argparse

# parse command line arguments
parser = argparse.ArgumentParser(description='dialog analysis script')
parser.add_argument('-o', 
                    dest='outputFile',
                    required=True,
                    help='output file name. Should be a .json file',
                    type=str
                    )
parser.add_argument('inputFile',
                    help='input file name. Should be a .csv file',
                    type=str
                    )
args = parser.parse_args()

# read input csv and preprocess (make pony names lowercase)
df = pd.read_csv(args.inputFile)
df['pony'] = df['pony'].str.lower() 

# make counts
ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
counts = {pony: df['pony'].value_counts()[pony] for pony in ponies}

# compute verbosity
num_rows = df.shape[0]
verbosities = {pony: "{:0.2f}".format(count/num_rows) for pony, count in counts.items()}

# create output json
output = { 
        "count": {k:str(v) for k, v in counts.items()}, 
        "verbosity": verbosities 
} 

print(output)

out_file = open(args.outputFile, "w") 
json.dump(output, out_file)
out_file.close() 
