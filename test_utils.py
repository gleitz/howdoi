import unittest
import math

from howdoi import utils


class TestUtils(unittest.TestCase):
    def test_get_top_n_from_dict_returns_correct_result(self):
        dictionary1 = {'a': 1, 'b': 2, 'd': 2, 'c': 11}
        top_2 = utils.get_top_n_from_dict(dictionary1, 2)

        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0], ('c', 11))
        self.assertEqual(top_2[1], ('d', 2))

    def test_safe_division(self):
        ans1 = utils.safe_divide(10, 3)
        self.assertTrue(math.isclose(ans1, 3.333, abs_tol=0.001))
        ans2 = utils.safe_divide(10, 0)
        self.assertEqual(ans2, 0)


if __name__ == '__main__':
    unittest.main()
