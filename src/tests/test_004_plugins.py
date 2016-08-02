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
import os

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))


class suite_plugins(unittest.TestCase):  #

    core = None
    ok = False
    counter = 0
    
    def setUp(self):
        sys.path.append(basepath)
        import core.core
        import time

        self.core = core.core.Core(name='core')
        self.core.start()
        while not self.core.ready:
            time.sleep(0.01)
        
    def tearDown(self):
        self.core.stop()
        
    def listener(self, **kw):
        self.counter += 1

    @pytest.mark.T1
    def test_0000_sample_plugin(self):
        
        import time
        
        t = time.time()
        while not self.core.plugins and time.time()-t < 10:
            time.sleep(0.1)

        plugin = self.core.plugins['sample']
        plugin.subscribe('sample/foo/*', self.listener)
        
        for i in range(0,10):
            # publish fake router notification!!
            # pylint: disable-msg = E1101
            plugin.publish(what='router/new_peer', address='localhost:9999', name='foo')
            # publish own notification
            # pylint: disable-msg = E1101
            plugin.publish(what='sample/foo', data=time.time())            
            time.sleep(0.1)
        
        self.assertEqual(self.counter, 10)
        
        
if __name__=='__main__':

    unittest.main()















