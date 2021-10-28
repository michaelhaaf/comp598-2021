import json, datetime
import os, sys
import argparse
import logging
from json.decoder import JSONDecodeError

# Python3: need to modify src.path to have consistent import behavior
# see https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.record import Record, RecordFactory, RecordException, RecordEncoder


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


## Usage
# python3 clean.py -i <input_file> -o <output_file>
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
