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
os.system("rm -f %s/tests/*.db" % basepath)
os.system("rm -f %s/*.db" % basepath)
os.system("rm -f ./*.db")

class suite_contacts(unittest.TestCase):  #

    core = None
    ok = False
    counter = 0
    
    def setUp(self):
        print ">>> rm -f %s/tests/*.db" % basepath
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
    def test_contacts(self):
        
        email = 'darthvader@gmail.com'
        
        contacts = self.core.contacts
        result = contacts.new_contact(rxtx='tx', email=email)
        self.assertTrue(result)

        # duplicated contact. Must fail
        result = contacts.new_contact(rxtx='tx', email=email)
        self.assertFalse(result)
        
        # contact is allready disabled
        result = contacts.remove_contact(email=email)
        self.assertFalse(result)
        
        # accept contact
        result = contacts.accept_contact(email=email)
        self.assertTrue(result)
        
        # contact allready accepted
        result = contacts.accept_contact(email=email)
        self.assertFalse(result)
        
        # unaccept contact
        result = contacts.remove_contact(email=email, delete_all=False)
        self.assertTrue(result)
        
        # contact is still there, but unacepted
        contact = contacts.get_contact(email=email)
        self.assertIsNotNone(contact)
        
        # remove completly contact
        result = contacts.remove_contact(email=email, delete_all=True)
        contact = contacts.get_contact(email=email)
        self.assertFalse(contact)
        
        # try to remove inexistant contact
        result = contacts.remove_contact(email='inexistant@inexistant.com', delete_all=True)
        self.assertFalse(result)
        
        # get contacts

        contacts = self.core.contacts
        result = contacts.new_contact(rxtx='tx', email='one@gmail.com')
        self.assertTrue(result)
        
        contacts = self.core.contacts
        result = contacts.new_contact(rxtx='tx', email='too@gmail.com')
        self.assertTrue(result)
        
        result = contacts.get_contacts()
        self.assertEqual(len(result), 2)
        
        result = contacts.get_contacts(which='accepted')
        self.assertEqual(len(result), 0)

        result = contacts.get_contacts(which='pending')
        self.assertEqual(len(result), 2)
                
        result = contacts.get_contacts(which='wrong condition')
        self.assertFalse(result)        
        
        return True
        
        
if __name__=='__main__':

    unittest.main()















