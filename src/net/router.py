#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Router module
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

import time

from utils import utils
from core import tserver
from core import zobject

log = utils.log

class Router(tserver.TServer, zobject.ZObject):

    '''
    Class Router. net has one instance of this
    '''
        
    remotes = {}
    port = None
    
    def __init__(self, *args, **kw):

        tserver.TServer.__init__(self, *args, **kw)
        zobject.ZObject.__init__(self, *args, **kw)

        self.port = kw['port']
        self._wakeup()
        
    def _wakeup(self):

        '''
        Wakes up router instance
        '''
        
        # pylint: disable-msg = E1101
        self.timer(name='purge', timer=60, method=self._purge)
        
    def get_address(self, who):
        '''
        Returns physical address of who if exists. else None
        '''
        remote = self.remotes.get(who)
        if remote:
            return remote['address']
        
    def update(self, name, address, **kw):

        '''
        Updates known and published addresses for name
        '''

        volatile = kw.get('volatile', True)
        info = kw.get('info')
        
        if not self.remotes.get(name):
            # pylint: disable-msg = E1101
            self.publish(what='router/new_peer', name=name, address=address)
            log.info("New Peer %s %s" % (name, str(address)))
        else:
            #log.info("Updated Peer %s %s" % (name, str(address)))
            pass
                    
        self.remotes.setdefault(name, {})
        self.remotes[name]['address'] = address
        self.remotes[name]['ts'] = time.time()

        if info:
            self.remotes[name]['info'] = info
            
        self.remotes[name].setdefault('volatile', volatile)
        
        
    def _purge(self, **kw):
        '''
        Removes remote information after time without news from him
        '''
        # pylint
        dummy = kw

        for k, remote in self.remotes.items():
            if remote['volatile'] and time.time() - remote['ts'] > 120:
                self.remotes.pop(k)
                # pylint: disable-msg = E1101
                self.publish(what='router/lostpeer', remote=remote)
                log.info("Lost peer %s" % k)
        
    def stop(self):
        '''
        Does specific stop tasks
        '''
        tserver.TServer.stop(self)
        
    
