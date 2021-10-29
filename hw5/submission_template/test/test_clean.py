import unittest
from pathlib import Path
import os, sys
import json

from src.clean import clean_record

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(__file__)

    # 1. posts that don’t have either “title” or “title_text” should be removed.
    def test_no_title_or_title_text_removed(self):

        # load test1 data
        fixture1_path = os.path.join(self.test_dir, 'fixtures', 'test_1.json')
        with open(fixture1_path) as f:
            test1_record = f.readline()
        
        # test  
        expectation = None
        result = clean_record(test1_record)

        # assert
        self.assertEqual(result, expectation)
        
    # 2. createdAt dates that don’t pass the ISO datetime standard should be removed.
    def test_non_ISO_datetime_compatible_removed(self):
        
        # load test2 data
        fixture2_path = os.path.join(self.test_dir, 'fixtures', 'test_2.json')
        with open(fixture2_path) as f:
            test2_record = f.readline()
        
        # test  
        expectation = None
        result = clean_record(test2_record)

        # assert
        self.assertEqual(result, expectation)
    
    # 3. Any lines that contain invalid JSON dictionaries should be ignored.
    def test_invalid_JSON_dict_removed(self):
        # load test3 data
        fixture3_path = os.path.join(self.test_dir, 'fixtures', 'test_3.json')
        with open(fixture3_path) as f:
            test3_record = f.readline()
        
        # test  
        expectation = None
        result = clean_record(test3_record)

        # assert
        self.assertEqual(result, expectation)
    
    # 4. Any lines for which "author" is null, N/A or empty.
    def test_null_author_removed(self):
        # load test4 data
        fixture4_path = os.path.join(self.test_dir, 'fixtures', 'test_4.json')
        with open(fixture4_path) as f:
            test4_record = f.readline()
        
        # test  
        expectation = None
        result = clean_record(test4_record)

        # assert
        self.assertEqual(result, expectation)

    # 5. total_count is a string containing a NON cast-able number ("twelve"), total_count is NOT cast to an int properly, instead the record is DISCARDED.
    def test_non_castable_total_count_removed(self):
        # load test5 data
        fixture5_path = os.path.join(self.test_dir, 'fixtures', 'test_5.json')
        with open(fixture5_path) as f:
            test5_record = f.readline()
        
        # test  
        expectation = None
        result = clean_record(test5_record)

        # assert
        self.assertEqual(result, expectation)
        
    # 6. The tags field gets split on spaces when given a tag containing THREE words (e.g., “nba basketball
    # game”).
    def test_tag_fields_split_on_spaces(self):
        # load test6 data
        fixture6_path = os.path.join(self.test_dir, 'fixtures', 'test_6.json')
        with open(fixture6_path) as f:
            test6_record = f.readline()
        
        # test  
        expectation = ["nba", "basketball", "game", "soccer"]
        record_under_test = clean_record(test6_record)

        # prepare for comparison then assert
        result = json.loads(record_under_test)['tags']
        self.assertEqual(result, expectation)
        
    ### MY CUSTOM TESTS ###

    # 7. Objects with 'title_text' field have field renamed to 'title'

    # 8. createdAt date time is standardized to UTC 

    # 9. createdAt alternative datetime format is supported

    # 10. Objects without 'author' field are removed

    # 11. Objects with empty 'author' field are removed

    # 12. Objects with null 'author' field are removed

    # 13. Objects with non int/float/str total_count are removed

    # 14. Objects with int/float/str total_count are cast to int

    # 15. Objects without tags/total_count are kept in the output

    
if __name__ == '__main__':
    unittest.main()
