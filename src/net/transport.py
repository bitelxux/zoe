#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Trasport base class
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

from utils import utils
from core import tserver
from core import zobject

log = utils.log

class Transport(tserver.TServer, zobject.ZObject):
    
    '''
    Base class
    '''
        
    def __init__(self, *args, **kw):
        
        tserver.TServer.__init__(self, *args, **kw)
        zobject.ZObject.__init__(self, *args, **kw)

    def send(self, msg, address):
        '''
        Virtual Method
        '''
        
        assert msg
        assert address
        
        log.warning("Virtual method !!")
    
    def attend(self, **kw):
        '''
        Virtual Method
        '''

        dummy = kw
        
        log.warning("Virtual method !!")
        
    def show_stats(self, **kw):
        '''
        Virtual Method
        '''
        
        dummy = kw        
        
        log.warning("Virtual method !!")

    def stop(self):
        '''
        do specific stop work and calls tserver stop
        '''
        
        tserver.TServer.stop(self)
        
    
