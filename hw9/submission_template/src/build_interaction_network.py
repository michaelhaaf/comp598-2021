#!/usr/bin/env python3

import pandas as pd
import numpy as np
import json
import argparse
from collections import Counter


BLACKLIST = ["other", "ponies", "and", "all"]
TOP_N_CHARS = 101


def load_data(path):
    df = pd.read_csv(path)
    df['pony'] = df['pony'].str.lower() 
    return df 


def build_char_list(df):
    raw_counts = dict(Counter(df.pony))
    filtered_counts = dict(filter(char_filter, raw_counts.items()))
    return sorted(filtered_counts, key=filtered_counts.get, reverse=True)[0:TOP_N_CHARS]


def char_filter(char):
    return not any(word in char[0] for word in BLACKLIST)


def build_network(df):
    character_list = build_char_list(df)
    network = initialize_network(character_list)

    temp = 0
    table = df.iterrows()
    for (i, row1), (j, row2) in zip(table, table):
        if (is_connected(row1, row2, character_list)):
            network[row1.pony][row2.pony] += 1 
            network[row2.pony][row1.pony] += 1 

    return network


def initialize_network(char_list):
    initial_network = {ch: {char:0 for char in char_list} for ch in char_list}
    return initial_network


def is_connected(dialog1, dialog2, character_list):
    valid_characters = dialog1.pony in character_list and dialog2.pony in character_list
    same_episode = dialog1.title == dialog2.title
    two_different_characters = dialog1.pony != dialog2.pony
    return valid_characters and same_episode and two_different_characters


def main(args):
    df = load_data(args.inputFile)

    network = build_network(df)

    out_file = open(args.outputFile, "w") 
    json.dump(network, out_file, indent=4)
    out_file.close() 


# USAGE:
# python build_interaction_network.py -i <script_input.csv> -o <output_file.json>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NLP network building script')
    parser.add_argument('-o', 
                        dest='outputFile',
                        required=True,
                        help='output file name. Should be a .json file',
                        type=str
                        )
    parser.add_argument('-i',
                        dest='inputFile',
                        required=True,
                        help='dialg file name. Should be a .csv file',
                        type=str
                        )
    args = parser.parse_args()
    main(args)

