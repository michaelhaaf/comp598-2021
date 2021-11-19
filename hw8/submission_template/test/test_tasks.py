import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

from src.compile_word_counts import load_data, compile_word_counts
import pandas
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
        # use self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        
        # setup
        df = load_data(self.mock_dialog)

        # test
        result = compile_word_counts(df)

        print(result)
        print(self.true_word_counts_json)
        # assert
        self.assertEqual(result, self.true_word_counts_json)


    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        self.assertTrue(True)
        
    
if __name__ == '__main__':
    unittest.main()
