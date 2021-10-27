import unittest
from pathlib import Path
import os, sys

from src.record import Record

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):
    def setUp(self):
        record = Record.Record()

    # 1. hosts that don’t have either “title” or “title_text” should be removed.
    def test_no_title_or_title_text_removed(self):
        # Just an idea for a test; write your implementation
        self.assertEqual(True, False)
        
    # 2. createdAt dates that don’t pass the ISO datetime standard should be removed.
    def test_non_ISO_datetime_compatible_removed(self):
        self.assertEqual(True, False)
    
    # 3. Any lines that contain invalid JSON dictionaries should be ignored.
    def test_invalid_JSON_dict_removed(self):
        self.assertEqual(True, False)
    
    # 4. Any lines for which "author" is null, N/A or empty.
    def test_null_author_removed(self):
        self.assertEqual(True, False)

    # 5. total_count is a string containing a cast-able number, total_count is cast to an int properly.
    def test_non_castable_total_count_removed(self):
        self.assertEqual(True, False)
        
    # 6. The tags field gets split on spaces when given a tag containing THREE words (e.g., “nba basketball
    # game”).
    def test_tag_fields_split_on_spaces(self):
        self.assertEqual(True, False)
        
    
if __name__ == '__main__':
    unittest.main()
