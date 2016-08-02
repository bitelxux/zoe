#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Protocol module
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

#Oops there is a problem with cjson encodes and RSA !!
#import cjson
import cPickle

from utils import utils
from core import zobject

log = utils.log

class Protocol(zobject.ZObject):
    
    '''
    Base protocol
    '''
    
    def __init__(self, **kw):

        kw.setdefault('name', 'protocol')
        zobject.ZObject.__init__(self, **kw)
        
    def encode(self, **kw):
        '''
        Virtual method
        '''

        dummy = kw
        
        log.info("Protocol.encode: Virtual method !!")
        assert False

    def decode(self, msg):
        '''
        Virtual method
        '''

        # pylint
        dummy = msg

        log.info("Protocol.decode: Virtual method !!")
        assert False
        

class Zoe(Protocol):
    '''
    Zoe is default protocol
    '''

    # pylint
    core = None
    
    def __init__(self, *args, **kw):
        
        Protocol.__init__(self, *args, **kw)
        
    def encode(self, **kw):
        '''
        Encodes message in Zoe protocol
        '''
        msg = dict()
        msg['cmd'] = kw['cmd']
        msg['mid'] = kw.get('mid', utils.hex_uuid())
        msg['from'] = self.core.my_id
        msg['to'] = kw.get('to')
        msg['payload'] = kw.get('payload')
        msg['signature'] = kw.get('signature')
        msg['msg_type'] = kw.get('msg_type')
        msg['encrypt'] = kw.get('encrypt', 0)
        msg = cPickle.dumps(msg)
        return msg
    
    def decode(self, msg):
        '''
        Decodes Zoe protocol message
        '''
        #msg = cjson.decode(msg)
        msg = cPickle.loads(msg)
        return msg
        
        
    
