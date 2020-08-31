#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lorawan_toa_cal import get_toa
import unittest

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_11(self):
        toa = get_toa(32, 12)["t_packet"]
        self.assertEqual( toa, 1810.432 )

    def test_12(self):
        toa = get_toa(32, 11)["t_packet"]
        self.assertEqual( toa, 987.136 )

    def test_13(self):
        toa = get_toa(32, 12, n_bw=250)["t_packet"]
        self.assertEqual( toa, 905.216 )

    def test_14(self):
        toa = get_toa(32, 12, n_bw=125, enable_auto_ldro=False, enable_ldro=True)["t_packet"]
        self.assertEqual( toa, 1810.432 )

    def test_21(self):
        toa = get_toa(64, 12, enable_eh=False)["t_packet"]
        self.assertEqual( toa, 2793.472 )

    def test_22(self):
        toa = get_toa(64, 12, enable_crc=False)["t_packet"]
        self.assertEqual( toa, 2793.472 )

    def test_31(self):
        toa = get_toa(12, 7)["t_packet"]
        self.assertEqual( toa, 41.216 )

    def test_41(self):
        toa = get_toa(12, 7, n_bw=500, enable_eh=False, enable_crc=False,
                      n_cr=4, n_preamble=6)["t_packet"]
        self.assertEqual( toa, 10.816 )

    def test_99(self):
        toa = get_toa(8, 12, n_bw=500,
                    enable_auto_ldro=False, enable_ldro=False,
                    enable_eh=False, enable_crc=True,
                    n_cr=1, n_preamble=6)["t_packet"]
        self.assertEqual( toa, 190.464 )

if __name__ == '__main__':
    unittest.main()
