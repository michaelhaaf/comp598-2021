#!/usr/bin/env python3

import pandas as pd
import json
import argparse
import string
import re
from collections import Counter

def load_stop_words():
    words = open("data/stopwords.txt", "r").read().split("\n")
    r = re.compile(r'^#')
    return {word for word in words if not bool(r.match(word))}

PUNCTUATION = '()[],-.?!;:#&'
MIN_COUNT = 5
STOP_WORDS = load_stop_words()  


def keep(word):
    return word.isalpha() and word not in STOP_WORDS


def word_counts(df):
    word_counter = Counter()
    df['dialog'].apply(lambda dialog: word_counter.update(preprocess(dialog)))
    return {word: count for (word, count) in word_counter.items() if count > MIN_COUNT}


def preprocess(dialog):
    punctuation_table = str.maketrans(PUNCTUATION, ' ' * len(PUNCTUATION))
    return filter(keep, dialog.lower().translate(punctuation_table).split(' '))


def main(args):
    # read input csv and preprocess pony names
    df = pd.read_csv(args.dialogFile)
    df['pony'] = df['pony'].str.lower() 

    # make word counts for each pony
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    counts = {pony: word_counts(df[df.pony == pony]) for pony in ponies}

    out_file = open(args.outputFile, "w") 
    json.dump(counts, out_file, indent=4)
    out_file.close() 


# USAGE:
# python compile_word_counts.py -o <word_counts_json> -d <dialog_csv>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dialog analysis script')
    parser.add_argument('-o', 
                        dest='outputFile',
                        required=True,
                        help='output file name. Should be a .json file',
                        type=str
                        )
    parser.add_argument('-d',
                        dest='dialogFile',
                        required=True,
                        help='dialg file name. Should be a .csv file',
                        type=str
                        )
    args = parser.parse_args()
    main(args)

