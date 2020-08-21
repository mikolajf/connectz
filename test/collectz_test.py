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
        print(tail, expected)
        self.assertEqual(main(filename), expected)

    # @parameterized.expand([
    #     (3, 3, 3, True)
    # ])
    # def test_valid_game_params(self, x, y, z, result):
    #     self.assertEqual(collectz.valid_game_params(x,y,z), result)

    # def test_valid_game_params(self):
    #     self.assertEqual(collectz.valid_game_params(3,3,3), True)
