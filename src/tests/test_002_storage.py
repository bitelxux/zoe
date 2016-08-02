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
sys.path.append(basepath)

os.system("rm -f %s/tests/*.db" % basepath)

class suite_storage(unittest.TestCase):  #
    
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

    @pytest.mark.T1
    def test_000_storage(self):
            
        storage = self.core.storage
        
        result, lapse = storage.wait_activity(method=storage.execute, sql="DELETE FROM contacts")
        
        result, lapse = storage.wait_activity(method=storage.new_contact, 
                                              id='fooo', 
                                              name='test', 
                                              rxtx='tx',
                                              email='pepito@gmail.com')
        self.assertTrue(result)
        
        contact, lapse = storage.wait_activity(method=storage.get_contact, name='test')
        self.assertTrue(contact)
        
        result, lapse = storage.wait_activity(method=storage.get_contact, email='pepito@gmail.com')
        self.assertTrue(contact)
        
        result, lapse = storage.wait_activity(method=storage.get_contact)
        self.assertFalse(result)

    @pytest.mark.T1
    def test_0010_wrong_sql(self):
            
        storage = self.core.storage
        
        result, lapse = storage.wait_activity(method=storage.execute, sql="DELExTE FROM contacts")
        self.assertEqual(result.get('affected'), storage.ERROR)
        
        
        
if __name__=='__main__':

    unittest.main()















