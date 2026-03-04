from unittest import TestCase

from rapt2.treebrd.utility import flatten


class TestFlatten(TestCase):
    def test_empty_list(self):
        self.assertEqual(flatten([]), [])

    def test_flat_list(self):
        self.assertEqual(flatten([1, 2, 3]), [1, 2, 3])

    def test_nested_list(self):
        self.assertEqual(flatten([1, [2, 3], 4]), [1, 2, 3, 4])

    def test_deeply_nested(self):
        self.assertEqual(flatten([1, [2, [3, [4]]]]), [1, 2, 3, 4])

    def test_all_nested(self):
        self.assertEqual(flatten([[1], [2], [3]]), [1, 2, 3])

    def test_mixed_nesting(self):
        self.assertEqual(flatten([[1, 2], 3, [4, [5, 6]]]), [1, 2, 3, 4, 5, 6])

    def test_single_element(self):
        self.assertEqual(flatten([1]), [1])

    def test_single_nested_element(self):
        self.assertEqual(flatten([[1]]), [1])

    def test_strings(self):
        self.assertEqual(flatten(["a", ["b", "c"]]), ["a", "b", "c"])
