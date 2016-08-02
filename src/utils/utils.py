#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
utils module
*******************************************************************

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

import hashlib
import datetime
import time
import threading
import ConfigParser
import smtplib
import ast
import netifaces
import uuid
import random
import socket
import os
import rsa

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='zoe.log', level=logging.DEBUG)
log = logging.getLogger()

# log too to stdout
log.addHandler(logging.StreamHandler())

class Singleton(type):
    '''
    Singleton metaclass
    '''
    _instances = {}
    def __call__(mcs, *args, **kwargs):
        if mcs not in mcs._instances:
            mcs._instances[mcs] = super(Singleton, mcs).__call__(*args, **kwargs)
        return mcs._instances[mcs]

class ZThread(threading.Thread):
    
    '''
    ZThread class
    '''
    
    name = None
    watchdog = None
    running = False
    
    def __init__(self, *args, **kw):
        assert 'name' in kw.keys()
        threading.Thread.__init__(self)
        self.running = False
        self.name = kw['name']
        
    def run(self):
        dummy = 1
        #self.running = True
        #print "%s ZThread running" % self.name
        #self.watchdog.im_alive(self.name)
        
    def is_running(self):
        '''
        Returns if current thread is running
        '''
        return self.running
    
    def stop(self):
        '''
        Stops current thread
        '''
        
        self.running = False

class Mailer(threading.Thread):
    
    '''
    Mailer helper
    '''
    
    _server = None
    _port = None
    _user = None
    _password = None
    _body = None
    _subject = None
    _to = None
    
    def __init__(self, *args, **kw):

        self.__dict__.update(**kw)
        threading.Thread.__init__(self)
        
    def send(self):
        '''
        Sends an email
        '''
        try:
            smtpserver = smtplib.SMTP(self._server, self._port)
            smtpserver.ehlo()
            # Oops matrix504 doesnt support ttls ...
            smtpserver.starttls()
            #smtpserver.ehlo
            smtpserver.login(self._user, self._password)
            header = 'To: %s\nFrom:"%s"\nSubject:%s\n' % (self._to, self._user, self._subject) 
            msg = header + '\n%s\n\n' % self._body            
            
            smtpserver.sendmail(self._user, self._to, msg)
            smtpserver.close()    
            log.info("mail sent to %s [%s]" % (self._to, self._subject))
            return True
        except Exception, why:
            log.error("Mailer: %s" % why)
            
            
def sendmail(**kw):
    '''
    Quick sendmail helper
    '''
    mailer = Mailer(**kw)
    result = mailer.send()
    return result
    
ALL_IFACES = '0.0.0.0'

class Net_Utils():
    '''
    Some networking adds
    '''

    def __init__(self):
        dummy = 1

    @staticmethod
    def ip_is_public( _ip=None ):
        '''
        based on http://www.faqs.org/rfcs/rfc1918.html
        returns if given ip is public or private
        10.0.0.0        -   10.255.255.255  (10/8 prefix)
        172.16.0.0      -   172.31.255.255  (172.16/12 prefix)
        192.168.0.0     -   192.168.255.255 (192.168/16 prefix)
        '''

        assert _ip

        if Net_Utils.ips_in_same_network( _ip, '10.0.0.0', '255.0.0.0' ):
            return False
        if Net_Utils.ips_in_same_network( _ip, '172.16.0.0', '255.255.0.0' ):
            return False
        if Net_Utils.ips_in_same_network( _ip, '192.168.0.0', '255.255.0.0' ):
            return False

        # Añadimos tambien localhost y parecidas
        if Net_Utils.ips_in_same_network( _ip, '127.0.0.0', '255.0.0.0' ):
            return False

        return True

    @staticmethod
    def get_ips(_skip_lo=True):
        '''
        Returns current IPs
        '''
        ifaces = []
        for iface_name in netifaces.interfaces():
            addresses = netifaces.ifaddresses( iface_name )
            if addresses.has_key( netifaces.AF_INET ):
                _ip = addresses[netifaces.AF_INET][0]['addr']
                if _ip != ALL_IFACES:
                    ifaces.append( _ip )

        if _skip_lo is True:
            if '127.0.0.1' in ifaces:
                ifaces.remove('127.0.0.1')

        return ifaces

    @staticmethod
    def get_ips_with_masks():
        '''
        Returns current Ips with their masks
        '''
        ifaces = []
        for iface_name in netifaces.interfaces():
            addresses = netifaces.ifaddresses( iface_name )
            if addresses.has_key( netifaces.AF_INET ):
                ifaces.append( (addresses[netifaces.AF_INET][0]['addr'], addresses[netifaces.AF_INET][0]['netmask'] ) )
        return ifaces


    @staticmethod
    def dottedQuadToNum(ip):
        '''
        Converts ip to number
        '''
        import struct
        # convert decimal dotted quad string to long integer
        try:
            return struct.unpack('L', socket.inet_aton(ip))[0]
        except Exception:
            return struct.unpack('I', socket.inet_aton(ip))[0]

    @staticmethod
    def numToDottedQuad(n):
        '''
        Converts long int into dotted quad string
        '''
        import struct
        # convert long int to dotted quad string
        try:
            return socket.inet_ntoa(struct.pack('L', n))
        except Exception:
            return socket.inet_ntoa(struct.pack('I', n))

    @staticmethod
    def ips_in_same_network(ip1, ip2, mask):
        '''
        Returns True if both IPs are in same network
        '''
        if '127.0.0.1' in (ip1, ip2,):
            return True
        num1 = Net_Utils.dottedQuadToNum(ip1)
        num2 = Net_Utils.dottedQuadToNum(ip2)
        nummask = Net_Utils.dottedQuadToNum(mask)
        return (num1 & nummask) == (num2 & nummask)

    
    
class ConfigManager():
    
    '''
    Config manager
    '''
    
    #__metaclass__ = Singleton
    
    config = None
    name = None
    ok = False
    
    def __init__(self, **kw):
        
        self.name = kw.get('name','config_manager')
        self.config_file = kw.get('config_file', 'config.cfg')
        self.config = ConfigParser.RawConfigParser()
        self.read_file()
        
    def read_file(self):
        
        '''
        Reads config file
        '''
        self.ok = self.config.read(self.config_file) 
        if not self.ok:
            print "No se pudo abrir %s" % self.config_file
            log.error(">>>>>>>>>> No se pudo abrir %s!!" % self.config_file)
            
    def get(self, section, what):

        '''
        Returns config value or None
        '''
        
        value = None
        self.read_file()
        
        try:
            value = self.config.get(section, what)
        except Exception, why:
            log.error("ConfigManager: %s" % why)
            
        return value
    
    def get_list(self, section, what):
        
        '''
        returns a list type value
        '''
            
        self.read_file()
        try:
            value = ast.literal_eval(self.config.get(section, what))
        except Exception, why:
            log.error("ConfigManager: %s" % why)
            value = None
        return value

    def get_int(self, section, what):
        
        '''
        returns int value
        '''
        
        value = None
        self.read_file()
        try:
            value = self.config.getint(section, what)
        except Exception:
            log.error('Not valid %s in section %s' %(what, section))
            
        return value
    
    def get_float(self, section, what):
        
        '''
        returns float value
        '''

        value = None
        self.read_file()
        try:
            value = self.config.getfloat(section, what)
        except Exception, why:
            log.error(why)
            
        return value

class RSA:    
    '''
    rsa helpers
    '''

    config = None
    name = None
    
    def __init__(self, **kw):
        self.config = kw.get('config')
    
    def check_rsa_keys(self):
        '''
        If rsa keys pair doesnt exists, creates them
        '''
        
        
        path = self.config.get('General', 'rsa') or './.rsa'
        if not os.path.exists(path):
            os.makedirs(path)
        
        my_id = self.config.get('General', 'id')
        priv = os.path.join(path, '%s.priv' % my_id)
        pub = os.path.join(path, '%s.pub' % my_id)
        
        if not os.path.exists(priv) or not os.path.exists(pub):
            
            # generate new keys
            (pubkey, privkey) = rsa.newkeys(512)
            
            # save keys
            pem = privkey.save_pkcs1('PEM')
            open(priv, 'w').write(pem)
    
            pem = pubkey.save_pkcs1('PEM')
            open(pub, 'w').write(pem)
            
            log.info("keys pair generated !!")
        else:
            print "RSA ok"
            
        # any way, fix permitions
        os.system("chmod -R 600 %s/*" % path)
        return True
    
    def rsa_sign(self, msg):
        '''
        generates msg sign with own priv key
        '''
        
        signature = None
    
        try:
            path = self.config.get('General', 'rsa')
            my_id = self.config.get('General', 'id')
            priv_file = os.path.join(path, '%s.priv' % my_id)
            privkey = rsa.PrivateKey.load_pkcs1(open(priv_file).read())
            
            signature = rsa.sign(msg, privkey, 'SHA-1')
        except Exception, why:
            log.error("Could not sign messge !! %s" % why)
            return
        
        return signature
        
    
    def encrypt(self, msg, to):
        '''
        encryts message with recipient public key
        '''
        
        try:
            path = self.config.get('General', 'rsa') or './.rsa'
            pubkey_file = os.path.join(path, '%s.pub' % to)
            pubkey = rsa.PublicKey.load_pkcs1(open(pubkey_file).read())
            
            msg = str(msg.encode('utf-8')) # deal with encoding ... so easy after hours ...
            
            crypted = rsa.encrypt(msg, pubkey)
            signature = self.rsa_sign(msg)
        except Exception, why:
            log.error("Could not encrypt messge !! %s" % why)
            return
        
        return crypted, signature
        
    
    def decrypt(self, msg, sender, signature):
        '''
        decrypts msg with own private key and checks sender signature
        '''
        try:
            path = self.config.get('General', 'rsa')
            my_id = self.config.get('General', 'id')
            
            priv_file = os.path.join(path, '%s.priv' % my_id)
            privkey = rsa.PrivateKey.load_pkcs1(open(priv_file).read())
    
            pub_file = os.path.join(path, '%s.pub' % sender) 
            pubkey_sender = rsa.PublicKey.load_pkcs1(open(pub_file).read())
            
            #uncrypt message
            uncrypted = rsa.decrypt(msg, privkey)
            
            # check remitent is who he says ...
            rsa.verify(uncrypted, signature, pubkey_sender)
        except Exception, why:
            log.error("Could not encrypt messge !! %s" % why)
            return
        
        # sender is comfirmed
        return uncrypted

    
def hex_uuid():
    '''
    Generates uuid
    example
    >>> uuid = uuid.uuid1()
    >>> uuid
    UUID('1548ab96-df2a-11e1-9804-78dd08e73185')
    >>> str(uuid).replace('-','')
    '1548ab96df2a11e1980478dd08e73185'
    '''
    return str(uuid.uuid1()).replace('-','')

def sha1(_string):
    '''
    Returns sha1 from string
    '''
    # pylint: disable-msg = E1101
    return hashlib.sha1(_string).hexdigest()

def randstring(_len=8):
    '''
    Generates a random alfanumeric string
    '''
    
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' 

    return ''.join([random.choice(chars) for _ in range(_len)])

def get_month_day(ts):
    '''
    returns day of the month from timestamp
    '''
    ts = datetime.datetime.fromtimestamp(ts)
    day = ts.strftime('%d')
    return day

def get_year(ts):
    '''
    returns year of the month from timestamp
    '''
    ts = datetime.datetime.fromtimestamp(ts)
    year = ts.strftime('%Y')
    return year

def get_month(ts):
    '''
    returns month of the month from timestamp
    '''
    
    ts = datetime.datetime.fromtimestamp(ts)
    month = ts.strftime('%m')
    return month

def get_week(ts):
    '''
    returns week of the month from timestamp
    '''
    
    ts = datetime.datetime.fromtimestamp(ts)
    week = ts.strftime('%W')
    return week

def fecha(format='"%Y-%m-%d %H:%M:%S"'):
    '''
    Helper to format current datetime to string date and time
    '''
    return datetime.datetime.now().strftime(format)    

def timestamp_2string(_ts, _format='%Y-%m-%d %H:%M:%S'):
    '''
    Helper to format timestamp to string date and time
    '''
    t = datetime.datetime.fromtimestamp(_ts)
    return t.strftime(_format)

def str_date_to_seconds(_date, _format='%Y-%m-%d %H:%M:%S'):
    '''
    Helper to format string date time to seconds
    '''
    a = datetime.datetime.strptime(_date, _format)
    return time.mktime(a.timetuple())
                    
def dhms_time(_time):
    '''
    Given ts returns years, months, days, hours, minutes, seconds
    '''
    
    t = _time
    dias = int(t/84600)
    resto = t - dias*84600
    horas = int(resto/3600)
    resto = resto - horas*3600
    minutos = int(resto/60)
    segundos = resto - minutos*60
        
    dhms = "%03dd:%02dh:%02dm:%02ds" % (dias, horas, minutos, segundos)
    return dhms                    
