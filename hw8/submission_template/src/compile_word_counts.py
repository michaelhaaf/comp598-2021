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


PONIES = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
PUNCTUATION = '()[],-.?!;:#&'
MIN_COUNT = 5
STOP_WORDS = load_stop_words()  


def load_data(path):
    df = pd.read_csv(path)
    df['pony'] = df['pony'].str.lower() 
    return df 


def compile_word_counts(df): 
    return {pony: word_counts(df[df.pony == pony]) for pony in PONIES}

    
def word_counts(df):
    word_counter = Counter()
    df['dialog'].apply(lambda dialog: word_counter.update(preprocess(dialog)))
    return {word: count for (word, count) in word_counter.items()}


def keep(word):
    return word.isalpha() and word not in STOP_WORDS


def preprocess(dialog):
    punctuation_table = str.maketrans(PUNCTUATION, ' ' * len(PUNCTUATION))
    return filter(keep, dialog.lower().translate(punctuation_table).split(' '))


# is there an elegant way to do this requirement? fundamentally strange
def postprocess(preprocessed_counts):
    # first, count our "valid speech acts" across all preprocessed acts
    overall_counter = Counter()
    for pony_dict in preprocessed_counts.values():
        overall_counter += Counter(pony_dict) 
    words_to_remove = [word for word, count in overall_counter.items() if count < MIN_COUNT]

    # create new counts without words < MIN_COUNT
    return { pony: {word: count for (word, count) in pony_dict.items() if word not in words_to_remove} 
            for pony, pony_dict in preprocessed_counts.items() }
        

def main(args):
    # read input csv and preprocess pony names
    df = load_data(args.dialogFile)

    # make word counts for each pony
    counts = compile_word_counts(df)
    postprocessed_counts = postprocess(counts)

    out_file = open(args.outputFile, "w") 
    json.dump(postprocessed_counts, out_file, indent=4)
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

