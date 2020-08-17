import unittest

from howdoi import utils


class TestUtils(unittest.TestCase):
    def test_get_top_n_from_dict_returns_correct_result(self):
        dictionary1 = {'a': 1, 'b': 2, 'd': 2, 'c': 11}
        top_2 = utils.get_top_n_from_dict(dictionary1, 2)

        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0], ('c', 11))
        self.assertEqual(top_2[1], ('d', 2))


if __name__ == '__main__':
    unittest.main()
