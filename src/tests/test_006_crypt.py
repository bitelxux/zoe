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
        
    def tearDown(self):
        pass
        
    def listener(self, **kw):
        self.counter += 1

    @pytest.mark.T1
    def test_0000_rsa(self):
        import rsa
        
        (pubkey, privkey) = rsa.newkeys(512)
        
        msg = 'hello there this is a crypted msg!!'
        crypted = rsa.encrypt(msg, pubkey)
        uncrypted = rsa.decrypt(crypted, privkey)
        self.assertEqual(uncrypted, msg)
 
    @pytest.mark.T1
    def test_0001_rsa_from_file(self):
        import rsa
        
        (pubkey_a, privkey_a) = rsa.newkeys(512)
        
        # save keys
        pem = privkey_a.save_pkcs1('PEM')
        open('/tmp/privada.a', 'w').write(pem)

        pem = pubkey_a.save_pkcs1('PEM')
        open('/tmp/publica.a', 'w').write(pem)

        (pubkey_b, privkey_b) = rsa.newkeys(512)
        
        # save keys
        pem = privkey_b.save_pkcs1('PEM')
        open('/tmp/privada.b', 'w').write(pem)

        pem = pubkey_b.save_pkcs1('PEM')
        open('/tmp/publica.b', 'w').write(pem)
        
        
        #load a keys
        pubkey_a = rsa.PublicKey.load_pkcs1(open('/tmp/publica.a').read())
        privkey_a = rsa.PrivateKey.load_pkcs1(open('/tmp/privada.a').read())

        pubkey_b = rsa.PublicKey.load_pkcs1(open('/tmp/publica.b').read())
        privkey_b = rsa.PrivateKey.load_pkcs1(open('/tmp/privada.b').read())

        # msg sent from b to a
        
        msg = 'hello there this is a crypted msg!!'
        
        signature = rsa.sign(msg, privkey_b, 'SHA-1')
        
        crypted = rsa.encrypt(msg, pubkey_a)
        uncrypted = rsa.decrypt(crypted, privkey_a)
        
        # check remitent is who he says ...
        rsa.verify(uncrypted, signature, pubkey_b)
        
        self.assertEqual(uncrypted, msg)
        
         
        
        
if __name__=='__main__':

    unittest.main()















