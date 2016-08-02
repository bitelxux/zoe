# -*- coding: utf-8  -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

This file is part of Zoe P2P.

Zoe P2P is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Zoe P2P is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Zoe P2P.  If not, see <http://www.gnu.org/licenses/>.
"""


import unittest
import pytest
import sys

basepath = '/home/cnn/Dropbox/personal/pfe/src/'

class suite_trivial(unittest.TestCase):  #

    def setUp(self):
        dummy = 1

    def tearDown(self):
        dummy = 1

    @pytest.mark.T1
    def test_000_trivial(self):
        self.assertTrue(True)

class suite_utils(unittest.TestCase):  #

    def setUp(self):
        sys.path.append(basepath)

    def tearDown(self):
        dummy = 1

    @pytest.mark.T1
    def _test_000_core_singleton(self):
        
        from core import core
        c1 = core.Core(name='core1')
        c2 = core.Core(name='core2')
        
        self.assertTrue(c1 is c2)

class suite_net_utils(unittest.TestCase):  #

    def setUp(self):
        sys.path.append(basepath)

    def tearDown(self):
        dummy = 1

    @pytest.mark.T1
    def test_000_get_ips(self):
        from utils import utils
        ips = utils.Net_Utils.get_ips()
        self.assertIsNotNone(ips)

    @pytest.mark.T1
    def test_000_get_ips_with_masks(self):
        from utils import utils
        ips = utils.Net_Utils.get_ips_with_masks()
        self.assertIsNotNone(ips)

        
        
if __name__=='__main__':

    unittest.main()















