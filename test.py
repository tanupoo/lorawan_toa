#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lorawan_toa import *
import unittest

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_1(self):
        self.assertEqual( get_toa(64, 12, bw=125, de=0), 2465.792000 )

    def test_2(self):
        self.assertEqual( get_toa(64, 12, bw=125, de=1), 2793.472000 )

    def test_3(self):
        self.assertEqual( get_toa(255, 7, bw=500, de=0), 99.904000 )

    def test_4(self):
        self.assertEqual( get_toa(255, 7, bw=500, de=1), 137.024 )

if __name__ == '__main__':
    unittest.main()
