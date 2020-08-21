import unittest
from collectz import main
from parameterized import parameterized
import glob
import os


class CollectzTest(unittest.TestCase):

    all_files = glob.glob('examples/*.txt')

    @parameterized.expand(all_files)
    def test_assessment_examples(self, filename):
        _, tail = os.path.split(filename)
        expected = int(tail[:1])
        self.assertEqual(main(filename), expected)
