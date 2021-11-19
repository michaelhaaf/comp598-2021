import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

from src.compile_word_counts import load_data, compile_word_counts
from src.compute_pony_lang import compute_pony_lang, idf

import pandas
import math
import json

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
         
        in_file = open(self.true_word_counts, "r")
        self.true_word_counts_json = json.load(in_file)
        in_file.close()

        in_file = open(self.true_tf_idfs, "r")
        self.true_tf_idfs_json = json.load(in_file)
        in_file.close()
        

    def test_task1(self):
        # setup
        df = load_data(self.mock_dialog)

        # test
        result = compile_word_counts(df)

        # assert
        self.assertEqual(result, self.true_word_counts_json)


    def test_task2(self):

        # test
        result = compute_pony_lang(self.true_word_counts_json, 2)

        # assert
        self.assertEqual(result, self.true_tf_idfs_json)

        # extra idf computation tests
        please_idf = idf("please", self.true_word_counts_json) 
        pretty_idf = idf("pretty", self.true_word_counts_json) 
        princess_idf = idf("princess", self.true_word_counts_json) 
        note_idf = idf("note", self.true_word_counts_json) 
        oyes_idf = idf("oyes", self.true_word_counts_json) 
        okie_idf = idf("okie", self.true_word_counts_json) 
        aaaaaaaa_idf = idf("aaaaaaaa", self.true_word_counts_json) 
        lol_idf = idf("lol", self.true_word_counts_json) 

        # assert 
        self.assertEqual(please_idf, math.log10( 6 / 2 ) )
        self.assertEqual(pretty_idf, math.log10( 6 / 2 ))
        self.assertEqual(princess_idf, math.log10( 6 / 1 ))
        self.assertEqual(note_idf, math.log10( 6 / 1 ))
        self.assertEqual(oyes_idf, math.log10( 6 / 4 ))
        self.assertEqual(okie_idf, math.log10( 6 / 1 ))
        self.assertEqual(aaaaaaaa_idf, math.log10( 6 / 1 ))
        self.assertEqual(lol_idf, math.log10( 6 / 1 ))


if __name__ == '__main__':
    unittest.main()
