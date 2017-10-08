#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lorawan_toa import *
import unittest

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_1(self):
        toa = get_toa(64, 12, n_bw=125, enable_dro=0)["t_packet"]
        self.assertEqual( toa, 2465.792000 )

    def test_2(self):
        toa = get_toa(64, 12, n_bw=125, enable_dro=1)["t_packet"]
        self.assertEqual( toa, 2793.472000 )

    def test_3(self):
        toa = get_toa(255, 7, n_bw=500, enable_dro=0)["t_packet"]
        self.assertEqual( toa, 99.904000 )

    def test_4(self):
        toa = get_toa(255, 7, n_bw=500, enable_dro=1)["t_packet"]
        self.assertEqual( toa, 137.024 )

if __name__ == '__main__':
    unittest.main()
