import unittest

import pytest

import mps_youtube.main as mps


class TestMain(unittest.TestCase):
    def test_fmt_time(self):
        pytest.skip('main not have tested attribute')
        self.assertEqual(mps.fmt_time(0), '00:00')
        self.assertEqual(mps.fmt_time(59), '00:59')
        self.assertEqual(mps.fmt_time(100), '01:40')
        self.assertEqual(mps.fmt_time(1000), '16:40')
        self.assertEqual(mps.fmt_time(5000), '83:20')
        self.assertEqual(mps.fmt_time(6500), '1:48:20')

    def test_num_repr(self):
        pytest.skip('main not have tested attribute')
        self.assertEqual(mps.num_repr(0), '0')
        self.assertEqual(mps.num_repr(1001), '1001')
        self.assertEqual(mps.num_repr(10001), '10k')
        self.assertEqual(mps.num_repr(100001), '100k')
        self.assertEqual(mps.num_repr(1000001), '1.0m')
        self.assertEqual(mps.num_repr(10000001), '10m')
        self.assertEqual(mps.num_repr(100000001), '100m')
        self.assertEqual(mps.num_repr(1000000001), '1.0B')

if __name__ == '__main__':
    unittest.main()
