import os, sys
import argparse
import json

def compute_average_title_lengths(reddit_json_list):
    title_lengths = [len(post['data']['title']) for post in reddit_json_list] 
    return sum(title_lengths) / len(title_lengths)

def main(args):

    # process input file
    with open(args.inputFile, "r") as in_file:
        input_data = [json.loads(line) for line in in_file]

    # process data
    average_length = compute_average_title_lengths(input_data) 

    # produce output 
    print(average_length)


## Usage
# python3 compute_title_lengths.py <input_file> 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='compute average title lengths from reddit json')
    parser.add_argument(
            help='input file name. Should be a .json file',
            type=str,
            dest='inputFile'
            )
    args = parser.parse_args()

    main(args)
