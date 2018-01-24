from unittest import TestCase

from annotator.data_set_util import get_data_set_group


class TestGet_data_set_group(TestCase):
    def test_get_data_set_group(self):
        self.assertEqual(get_data_set_group(0), 0)
        self.assertEqual(get_data_set_group(1), 0)
        self.assertEqual(get_data_set_group(2), 0)
        self.assertEqual(get_data_set_group(3), 0)
        self.assertEqual(get_data_set_group(4), 0)
        self.assertEqual(get_data_set_group(5), 0)
        self.assertEqual(get_data_set_group(6), 0)
        self.assertEqual(get_data_set_group(7), 0)
        self.assertEqual(get_data_set_group(8), 1)
        self.assertEqual(get_data_set_group(9), 2)
        self.assertEqual(get_data_set_group(10), 0)
