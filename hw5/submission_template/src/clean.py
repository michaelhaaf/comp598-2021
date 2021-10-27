## Requirements
# 1. Remove all posts that don't have title or or title_text
# 2. Standardize createdAt to UTC
# 3. Rename title_text field to title
# 4. Remove posts that cannot be standardized to UTC
# 5. Remove invalid JSON dicts
# 6. Remove posts with empty/null/N/A author field
# 7. total_count must be int, float, str. Cast float/str to int. If it cannot be int, remove.
# 8. Remove posts where total_count is not int,float,str. Except, if total_count is missing, keep the JSON object.
# 9. tags field needs to be list of words (but keep the record if tags is missing). Split words separated by spaces into two separate words ["football games"] -> ["football", "games"]
# 10. Posts not flagged for removal should be written to output file in order they appear in input file.

## Usage
# python3 clean.py -i <input_file> -o <output_file>


import json, datetime
import os, sys
import argparse
import record

# parse command line arguments
parser = argparse.ArgumentParser(description='json cleaner script')
parser.add_argument('-i',
        required=True,
        help='input file name. Should be a .json file',
        type=str,
        dest='inputFile'
        )
parser.add_argument('-o',
        required=True,
        help='output file name. Should be a .json file',
        type=str,
        dest='outputFile'
        )
args = parser.parse_args()

# process input file
in_file = open(args.inputFile, "r")
input_data = in_file.readlines()
in_file.close()

# process data
# TODO: replace with list comprehension
output_data = []
for input_line in input_data:
    output_line = Record.fromJson(input_line)
    if output_line is not None:
        output_data.append(output_line)
        
# produce output file
out_file = open(args.outputFile, "w")
out_file.writelines(output_data)
out_file.close()

