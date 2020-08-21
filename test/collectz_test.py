import unittest
from collectz import main
from parameterized import parameterized
import glob
import os


class CollectzTest(unittest.TestCase):

    all_files = glob.glob('examples/*.txt')

    @parameterized.expand(all_files)
    def test_file(self, filename):
        _, tail = os.path.split(filename)
        expected = int(tail[:1])
        self.assertEqual(main(filename), expected)
        
    def test_invalid_file(self):
        self.assertEqual(main("dsaffas.txt"), 9)
