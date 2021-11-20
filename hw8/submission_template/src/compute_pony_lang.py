import os, sys
import argparse
import json
import math


def idf(word, pony_counts):
    ponies_that_used_word_count = sum([1 for pony in pony_counts if word in pony_counts[pony]])
    return math.log10( len(pony_counts.keys()) / ponies_that_used_word_count )


def top_n_tf_idf(pony, pony_counts, n):
    tf_idf_scores = { word: count * idf(word, pony_counts) for word, count in pony_counts[pony].items() }
    return sorted(tf_idf_scores, key=tf_idf_scores.get, reverse=True)[0:n]


def compute_pony_lang(pony_counts, num_words): 
    return {pony: top_n_tf_idf(pony, pony_counts, num_words) for pony in pony_counts.keys()}


def main(args):
    in_file = open(args.pony_counts, "r")
    pony_counts = json.load(in_file)
    in_file.close()

    results = compute_pony_lang(pony_counts, args.num_words)

    print(json.dumps(results, indent=4))


# USAGE:
# python compute_pony_lang.py -c <word_counts_json> -n <num_words>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='compute frequency and distinctive pony language use')
    parser.add_argument('-c', 
                        dest='pony_counts',
                        required=True,
                        help='input file name. Should be a .json with word count dicts for each pony',
                        type=str
                        )
    parser.add_argument('-n',
                        dest='num_words',
                        required=True,
                        help='the top n words to report tf-idf for each pony',
                        type=int
                        )
    args = parser.parse_args()
    main(args)

