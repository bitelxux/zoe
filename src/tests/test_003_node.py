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

class suite_node(unittest.TestCase):  #
    
    os.system("rm -f %s/tests/*.db" % basepath)

    core = None
    
    def setUp(self):
        sys.path.append(basepath)
        import core.core
        import time

        self.core = core.core.Core(name='core')
        self.core.start()
        while not self.core.ready:
            time.sleep(0.01)
        storage = self.core.storage
        self.core.storage.activity(wait=10, method=storage.execute, sql='DELETE FROM messages')
        
    def tearDown(self):
        self.core.stop()

    @pytest.mark.T1
    def test_0000_foo(self):
        assert True
        
    @pytest.mark.T1
    def test_0010_new_contact(self):
        import time
        from utils import utils

        node = self.core.node
        
        name = utils.randstring(5)
        surname = utils.randstring(8)
        complete_name = '%s %s' %(name, surname)
        
        email = ('%s%s@gmail.com' %(name[:1], surname) ).lower()
        
        result = node.invite_contact(email=email)
        self.assertTrue(result)
        
        return True

    @pytest.mark.T1
    def test_0020_new_message(self):
        import time
        from utils import utils

        node = self.core.node
        
        msg = 'asdfasdf asfasf asdf asdfasdfs adfasdf'
                
        # message to not contact. Must fail
        result = node.new_message(recipient='foo', body=msg)
        self.assertFalse(result[0])
        
        # create and accept contact, then send
        
        email = 'foo@gmail.com'
        
        contacts = self.core.contacts
        result = contacts.new_contact(rxtx='tx', email=email)
        self.assertTrue(result)

        # accept contact
        result = contacts.accept_contact(email=email)
        self.assertTrue(result)       

        # message to acepted contact. 
        result, text = node.new_message(recipient=email, body=msg)
        self.assertTrue(result)
        
        return True
        
    
        
if __name__=='__main__':

    unittest.main()















