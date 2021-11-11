import argparse
import json
import os, sys
import pandas as pd
from pathlib import Path

def main(args):
    
    # process input file
    print(f"Loading annotations from {args.coded_file}...")
    with open(args.coded_file, "r") as in_file:
        df = pd.read_csv(in_file, sep='\t', header=0)


    # count annotations
    output_dict = {}
    output_dict['course-related'] = int(df['coding'].value_counts().get('c', 0))
    output_dict['food-related'] = int(df['coding'].value_counts().get('f', 0))
    output_dict['residence-related'] = int(df['coding'].value_counts().get('r', 0))
    output_dict['other'] = int(df['coding'].value_counts().get('o', 0))

    # print to file/stddout
    if args.out_file:
        with safe_open(args.out_file, "w") as out_file:
            json.dump(output_dict, out_file)
        print(f"Printed output to {args.out_file}")
    else:
        print(output_dict)

    
# helper method inspired by: https://stackoverflow.com/a/23794010
# Open "path" for writing, creating any parent directories as needed.
def safe_open(filename, mode):
    path = Path(filename).resolve()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, mode)


## Usage
# python3 analyze.py -i <coded_file.tsv> [-o <output_file>]
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='accepts annotated tsv file, outputs the number of each category. Optional output file. Prints to stdout if no output specified.')
    parser.add_argument('-o',
            required=False,
            help='output json file',
            type=str,
            dest='out_file'
            )
    parser.add_argument('-i',
            required=True,
            help='input annotated tsv file',
            type=str,
            dest='coded_file'
            )
    args = parser.parse_args()

    main(args)
