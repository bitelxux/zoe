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



import random
import unittest
import pytest
import sys
import os

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

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
        from utils import utils
        self.utils = utils

    def tearDown(self):
        dummy = 1

    @pytest.mark.T1
    def test_000_singleton(self):
        
        class foo:
            __metaclass__ = self.utils.Singleton
            def __init__(self):
                dummy = 1
            
        c1 = foo()
        c2 = foo()
        
        self.assertTrue(c1 is c2)
        
    @pytest.mark.T1
    def test_0010_ZThread(self):
        
        z_thread = self.utils.ZThread(name='foo')
        z_thread.run()
        z_thread.running = True
        result = z_thread.is_running()
        self.assertTrue(result)
        z_thread.stop()
        
    @pytest.mark.T1
    def test_0020_Mailer(self):
        
        result = self.utils.sendmail(_server='smtp.gmail.com',
                                     _port = 587,
                                     _user = 'darz.vather@gmail.com',
                                      _password = '1dvd=6divx',
                                     _to='bitelxux@gmail.com', 
                                     _subject='test_0020_Mailer at jenkins',
                                     _body='body')
        
        self.assertTrue(result)

        # this will fail as password is wrong
        result = self.utils.sendmail(_server='smtp.gmail.com',
                                     _port = 587,
                                     _user = 'darz.vather@gmail.com',
                                     _password = 'wrongpass',
                                     _to='bitelxux@gmail.com', 
                                     _subject='Failed test',
                                     _body='body')
        
        self.assertFalse(result)
        
        
    @pytest.mark.T1
    def test_0030_sha1(self):
        
        wanted = '3b03ce15d12325f8966f3f9530185625c5c4496f'
        text = "May the Fprce be with you ..."
        sha = self.utils.sha1(text)
        self.assertEqual(sha, wanted)
    
    @pytest.mark.T1
    def test_0040_rand_string(self):
        
        result = self.utils.randstring()
        self.assertEqual(len(result), 8)
        
        _len = random.randint(0,50)
        
        result = self.utils.randstring(_len=_len)
        self.assertEqual(len(result), _len)
        
    @pytest.mark.T1
    def test_0050_date_parts(self):
        ts = 14574600 # "1970-06-18 17:30:00
        
        month_day = self.utils.get_month_day(ts)
        year = self.utils.get_year(ts)
        month = self.utils.get_month(ts)
        week = self.utils.get_week(ts)
        
        self.assertEqual(month, '06')
        self.assertEqual(year, '1970')
        self.assertEqual(week, '24')
        self.assertEqual(month_day, '18')

    @pytest.mark.T1
    def test_0060_str_date_to_seconds(self):
        
        wanted = 14574600
        fecha = "1970-06-18 17:30:00"
        seconds = self.utils.str_date_to_seconds(fecha)
        
        self.assertEqual(seconds, wanted)
   
    @pytest.mark.T1
    def test_0070_timestamp_to_string(self):
        
        seconds = 14574600
        wanted = "1970-06-18 17:30:00"
        result = self.utils.timestamp_2string(seconds)
        
        self.assertEqual(result, wanted)        

    @pytest.mark.T1
    def test_0080_dhms_time(self):
        
        wanted = '172d:06h:30m:00s'
        seconds = 14574600
        result = self.utils.dhms_time(seconds)
        self.assertEqual(result, wanted)
        
    @pytest.mark.T1
    def test_0090_fecha(self):
    
        result = self.utils.fecha()
        self.assertIsNotNone(result)
        
        
class suite_net_utils(unittest.TestCase):  #

    def setUp(self):
        sys.path.append(basepath)
        from utils import utils
        self.utils = utils

    def tearDown(self):
        dummy = 1

    @pytest.mark.T1
    def test_0000_instance(self):
        net = self.utils.Net_Utils()
        self.assertIsNotNone(net)
        
    @pytest.mark.T1
    def test_0001_ip_is_public(self):
        
        result = self.utils.Net_Utils.ip_is_public('8.8.8.8')
        self.assertTrue(result)
        result = self.utils.Net_Utils.ip_is_public('10.0.10.1')
        self.assertFalse(result)
        result = self.utils.Net_Utils.ip_is_public('127.16.1.1')
        self.assertFalse(result)
        result = self.utils.Net_Utils.ip_is_public('192.168.20.10')
        self.assertFalse(result)
        result = self.utils.Net_Utils.ip_is_public('172.16.20.10')
        self.assertFalse(result)
        
    @pytest.mark.T1
    def test_0010_get_ips(self):
        from utils import utils
        ips = utils.Net_Utils.get_ips()
        self.assertIsNotNone(ips)

    @pytest.mark.T1
    def test_0020_get_ips_with_masks(self):
        from utils import utils
        ips = utils.Net_Utils.get_ips_with_masks()
        self.assertIsNotNone(ips)

    @pytest.mark.T1
    def test_0030_dottedQuadToNum(self):
        ip = '192.168.1.1'
        num = self.utils.Net_Utils.dottedQuadToNum(ip)
        self.assertEqual(num, 16885952)    
        
    @pytest.mark.T1
    def test_0040_numToDottedQuad(self):
        num = 16885952
        ip = self.utils.Net_Utils.numToDottedQuad(num)
        self.assertEqual(ip, '192.168.1.1')
        
    @pytest.mark.T1
    def test_0040_same_network(self):
        
        result = self.utils.Net_Utils.ips_in_same_network('192.168.1.1', '192.168.1.2', '255.255.255.0')
        self.assertTrue(result)
        
        result = self.utils.Net_Utils.ips_in_same_network('192.168.1.1', '127.0.0.1', '255.255.255.0')
        self.assertTrue(result)
        
        result = self.utils.Net_Utils.ips_in_same_network('192.168.2.1', '192.168.1.2', '255.255.255.0')
        self.assertFalse(result)
        
        result = self.utils.Net_Utils.ips_in_same_network('192.168.2.1', '192.168.1.2', '255.255.0.0')
        self.assertTrue(result)
        
class suite_config_manager(unittest.TestCase):  #

    file_name = None
    
    def setUp(self):
    
        sys.path.append(basepath)
        import os
        
        file_name = os.path.join(os.path.dirname(__file__),'config.cfg')
        
        from utils import utils
        self.config = utils.ConfigManager(name='config', config_file=file_name)

    def tearDown(self):
        dummy = 1

    @pytest.mark.T1
    def test_0000_get(self):
        
        value = self.config.get('General', 'id')
        self.assertEqual(value, 'bitelxux@gmail.com')
        
        value = self.config.get('Inexistant', 'foo')
        self.assertFalse(value)
        
        value = self.config.get('General', 'inexistant')
        self.assertFalse(value)
        
        value = self.config.get_int('Console', 'port') 
        self.assertEqual(value, 6666)
        
        value = self.config.get_int('General', 'log_file')
        self.assertEqual(value, None)

        value = self.config.get_float('Test', 'flotante')
        self.assertEqual(value, 12.32)
        
        value = self.config.get_float('Test', 'lista1')
        self.assertFalse(value)
        
    @pytest.mark.T1
    def test_008_fail_open(self):
        
         from utils import utils
         self.config = utils.ConfigManager(name='config', config_file='does.not.exist')
         self.assertFalse(self.config.ok)

        
    @pytest.mark.T1
    def test_0010_get_list(self):

        wanted1 = ['uno', 'dos', 23.2, False, 5]
        wanted2 = ('uno', 'dos', 23.2, False, 5)
        wanted3 = {'a':1, 'b':2}
        
        lista1 = self.config.get_list('Test', 'lista1')
        lista2 = self.config.get_list('Test', 'lista2')
        lista3 = self.config.get_list('Test', 'lista3')
        
        self.assertEqual(lista1, wanted1)
        self.assertEqual(lista2, wanted2)
        self.assertEqual(lista3, wanted3)
        
        lista4 = self.config.get_list('Mail', 'user')
        self.assertIsNone(lista4)

class suite_rsa_utils(unittest.TestCase):  #

    def setUp(self):
        sys.path.append(basepath)
        
        file_name = os.path.join(os.path.dirname(__file__),'config.cfg')
        print ">>><>>>> file_name = %s" % file_name
        
        from utils import utils
        config = utils.ConfigManager(name='config', config_file=file_name)
        self.rsa_manager = utils.RSA(config=config)
        
    def tearDown(self):
        dummy = 1

    @pytest.mark.T1
    def test_0000_rsa(self):
        result = self.rsa_manager.check_rsa_keys()
        self.assertTrue(result)
        
    @pytest.mark.T1
    def test_0010_rsa_encrypt_decrypt(self):
        msg = 'hello there !!'
        to = 'bitelxux@gmail.com'
        
        crypted, signature = self.rsa_manager.encrypt(msg, to)
        self.assertIsNotNone(crypted)
        self.assertIsNotNone(signature)
        
        plain = self.rsa_manager.decrypt(crypted, 'bitelxux@gmail.com', signature)
        self.assertEqual(plain,msg)
        
        
if __name__=='__main__':

    unittest.main()















