import argparse
import json
import os, sys
import pandas as pd

def main(args):
    
    # process input file
    print(f"Loading annotations from {args.coded_file}...")
    with open(args.coded_file, "r") as in_file:
        input_data = pd.read_csv(in_file, sep='\t', header=0)


    # count annotations

    # print to file/stddout

    print("Finished!")
    

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
            help='input annotated tsv file',
            type=str,
            dest='coded_file'
            )
    args = parser.parse_args()

    main(args)
