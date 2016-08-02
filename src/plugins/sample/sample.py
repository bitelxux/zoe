#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Zoe plugin sample
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

import os

from utils import utils
from core import tserver
from core import zobject

log = utils.log

class Sample(tserver.TServer, zobject.ZObject):

    '''
    Sample plugin class
    '''

    running = False  
    config = None
    basepath = None

    pause = 0

    # pylint
    core = None
    name = None
    
    def __init__(self, *args, **kw):
        
        tserver.TServer.__init__(self, *args, **kw)
        zobject.ZObject.__init__(self, *args, **kw)
                
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        
        self.config = utils.ConfigManager(config_file='%s/config.cfg' % self.basepath)

        #Timer example
        #self.timer(name='sample', timer=1.0, method=self.test)    

        # pylint: disable-msg = E1101
        self.timer(name='load_config', timer=30, method=self.load_config)

        # subscription example. User regulars
        self.subscribe('router/new_peer/*', self.new_peer)    
        self.subscribe('net/new_message/*', self.new_message)

    def new_message(self, **kw):
        '''
        sample public method
        '''

        # launch activity so listener doesn't use publisher thread
        # pylint: disable-msg = E1101
        self.activity(wait=30, method=self._new_message, **kw)
        
        
    def new_peer(self, **kw):
        '''
        sample public method
        '''

        # launch activity so listener doesn't use publisher thread
        # pylint: disable-msg = E1101
        self.activity(wait=30, method=self._new_peer, **kw)

    def _new_peer(self, **kw):
        '''
        Sample private method called from public one
        '''
        
        node_id = self.core.my_id
        log.info("Sample-%s Plugin: New peer %s %s" % (node_id, kw['address'], kw['name']))

    def _new_message(self, **kw):
        '''
        Sample private method called from public one
        '''
        
        node_id = self.core.my_id
        msg = kw['msg']
        log.info("Sample-%s Plugin: New message from %s : %s" % (node_id, msg['from'], msg['payload']))
        
    def stop(self, **kw):
        '''
        Specific stop tasks
        '''
        # pylint
        dummy = kw

        tserver.TServer.stop(self)
        log.info("%s stopped" % self.name)

    def load_config(self, **kw):
        '''
        loads config
        '''
        #pylint
        dummy = kw

        #print "%s loading config" % self.name
        self.pause = self.config.get_float('General', 'pause')


