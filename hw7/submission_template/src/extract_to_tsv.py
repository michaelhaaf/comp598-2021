import argparse
import json
import os, sys
import random
import csv

def main(args):
    
    # process input file
    print(f"Loading posts from {args.json_file}...")
    with open(args.json_file, "r") as in_file:
        input_data = [json.loads(line) for line in in_file]

    # random selection of k elements
    if len(input_data) > args.num_posts_to_output:
        k = args.num_posts_to_output
    else:
        k = len(input_data)

    print(f"Selecting {k} random posts from {args.json_file}...")
    chosen_posts = random.sample(input_data, k)

    # Write tsv file
    print(f"Writing random selected posts to {args.out_file}...")
    with safe_open_w(args.out_file, 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['Name', 'title', 'coding'])
        for line in chosen_posts:
            tsv_writer.writerow([line['data']['name'], line['data']['title'], ''])

    print("Finished!")
    

# helper method inspired by: https://stackoverflow.com/a/23794010
# Open "path" for writing, creating any parent directories as needed.
def safe_open_w(path, mode):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, mode)


## Usage
# python3 extract_to_tsv.py -o <out_file> <json_file> <num_posts_to_output>
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='accepts line separated json file from Reddit, outputs a random selection of posts from that file to a tsv')
    parser.add_argument('-o',
            required=True,
            help='output tsv file',
            type=str,
            dest='out_file'
            )
    parser.add_argument(
            help='input json file',
            type=str,
            dest='json_file'
            )
    parser.add_argument(
            help='number of posts to output',
            type=int,
            dest='num_posts_to_output'
            )
    args = parser.parse_args()

    main(args)
