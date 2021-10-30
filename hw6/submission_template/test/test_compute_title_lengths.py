import unittest
from pathlib import Path
import os, sys, io
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

from src.compute_title_lengths import main
import argparse

class ComputeTitleLengthsTest(unittest.TestCase):
    def setUp(self):
        self.compute_title_lengths_file_path = os.path.join(parentdir, 'src', 'compute_title_lengths.py')
        self.test_fixture_file_path = os.path.join(parentdir, 'test', 'fixtures', 'test_sample.json')
        print("\nRUNNING TESTS FOR HW6: COMPUTE TITLE LENGTHS")

        
    def test_compute_title_lengths_correct_result_for_given_sample(self):
        print(f"Ensure compute_title_lengths.py computes correct average for given sample")
        print(self.test_fixture_file_path)

        ## set up: provide sample file, which has 2 titles and an average length of :
        # title 1: "I see you choosing the hard way" -- 31 characters
        # title 2: "Salvatore Ganacci - Boycycle" -- 28 characters
        parser = argparse.ArgumentParser()
        parser.add_argument(dest='inputFile',type=str)
        argv = [self.test_fixture_file_path]
        args = parser.parse_args(argv)
        self.assertEqual(args.inputFile, self.test_fixture_file_path)

        # test: using stdout capture
        capturedOutput = io.StringIO() 
        sys.stdout = capturedOutput    
        main(args)                      
        sys.stdout = sys.__stdout__      
        result = str(capturedOutput.getvalue()).replace('\n', '')

        # compare
        expectation = ( 31 + 28 ) / 2
        self.assertEqual(result, str(expectation))
        print("OK")


    def tearDownClass():
        print("\n\nYou are all set! <3")
    
if __name__ == '__main__':
    unittest.main()
