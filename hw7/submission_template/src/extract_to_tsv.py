import argparse
import json
import os, sys


def main(args):
    print(args.out_file)
    print(args.json_file)
    print(args.num_posts_to_output)


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
            type=str,
            dest='num_posts_to_output'
            )
    args = parser.parse_args()

    main(args)
