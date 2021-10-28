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
import logging

from src.record import Record, RecordFactory, RecordException, RecordEncoder

from json.decoder import JSONDecodeError

def clean_record(input_string):
    """Clean a JSON according to HW5 requirements.
    Uses the Record class to enforce business logic

    Keyword arguments:
    input_string -- any string, if not a valid JSON, method will return None

    Output:
    - if record can be cleaned: a valid JSON string with clean data
    - else, the None object will be returned 
    """
    try:
        input_dict = json.loads(input_string)
    except JSONDecodeError as e:
        logging.info(f"Invalid JSON: {input_string}", e)
        return None

    try:
        record = RecordFactory.from_dictionary(input_dict)
    except RecordException as e:
        logging.info("Invalid input_dict: {input_dict}", e)
        return None

    return json.dumps(record, cls=RecordEncoder)


def main(args):

    # process input file
    in_file = open(args.inputFile, "r")
    input_data = in_file.readlines()
    in_file.close()

    # process data
    output_data = [clean_record(input_line) for input_line in input_data if clean_record(input_line) is not None]
            
    # produce output file
    out_file = open(args.outputFile, "w")
    out_file.writelines(output_data)
    out_file.close()


if __name__ == "__main__":

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

    main(args)
