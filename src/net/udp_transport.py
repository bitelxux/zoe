#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
UDPTransport module
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

import socket
import select

from utils import utils
from core import zobject
from . import transport

log = utils.log

class RX_thread(utils.ZThread, zobject.ZObject):
    
    '''
    Specific and dedicated RX thread
    '''
    
    caller = None
    wakeup = None
    wakeup_port = None
    fd = None
    
    def __init__(self, *args, **kw):
        self.caller = kw['caller']
        self.fd = self.caller.fd
        self.wakeup = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.wakeup.setblocking(0)
        self.running = False
        
        zobject.ZObject.__init__(self, *args, **kw)
        utils.ZThread.__init__(self, *args, **kw)
        
        
    def run(self):

        '''
        Udp transport loop
        '''
        
        self.running = True
        
        # send a packet to get port assigned
        self.wakeup.sendto('foo', ('localhost', 2222))
        self.wakeup_port = self.wakeup.getsockname()[1]
        
        while self.running:
            utils.ZThread.run(self)
            try:
                rx, _, _ = select.select([self.fd, self.wakeup], [], [], 5.0)
                if self.wakeup in rx:
                    self.wakeup.close()
                elif self.fd in rx:
                    raw, address = self.fd.recvfrom(0xFFFF)
                    #log.info(" <<<<<<<<<<<<<< recibido de %s" % str(address))
                    self.caller.attend(raw=raw, address=address)
            except Exception, why:
                log.warning("udp_transport %s" % why)
                
                
    def stop(self):
        '''
        Specific stop tasks
        '''
        self.wakeup.sendto('wakeup', ('localhost', self.wakeup_port))
        utils.ZThread.stop(self)
        
class UDPPtransport(transport.Transport):
    
    '''
    Transport based on UDP sockets
    '''
        
    fd = None
    fd_port = None
    rx_thread = None
    
    compress = False

    stats = {'rx':0, 'tx':0}
    
    def __init__(self, *args, **kw):
        transport.Transport.__init__(self, *args, **kw)
        self.core = kw['core']
        self.wakeup()
        
    def wakeup(self):

        '''
        wakeup instance
        '''
        

        self.renew_fd()
        # pylint: disable-msg = E1101
        self.rx_thread = RX_thread(core=self.core, name='rx_thread', caller=self)
        self.rx_thread.start()
        
        self.timer(name='stats', timer=5, method=self.show_stats)
        
    def get_local_address(self):
        '''
        Returns local fd fhysical address
        '''
        return self.fd.getsockname()
        
    def renew_fd(self):
        '''
        Renews fd
        '''
        
        if self.rx_thread:
            self.rx_thread.stop()
        
        if self.fd:
            self.fd.close()
            
        self.fd_port = self.core.configManager.get_int('General', 'udp_port')
            
        self.fd = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        
        if self.fd_port:
            self.fd.bind(('0.0.0.0', self.fd_port))
        else:
            self.fd.sendto('dummy', ('localhost', 2222))
            self.fd_port = self.fd.getsockname()[1]
            
        log.info("UDP listening on port %d" % self.fd_port )
            
        self.fd.setblocking(0)
        self.fd.settimeout( 600.0  )
        
    def _send(self, **kw):

        '''
        sends msg through fd
        '''
        
        address = kw['address']
        msg = kw['msg']
        
        self.stats['tx'] += len(msg)
        self.fd.sendto(msg , address)
        
        #log.info(" >>>>>>>>>>>>>>> enviado a %s" % str(address))
                
    def send(self, msg, address):
        '''
        Pyblic send method
        '''
        # pylint: disable-msg = E1101
        self.activity(wait=30, method=self._send, msg=msg, address=address)
        dummy = 1
        
    def stop(self):
        '''
        Stop specific tasks
        '''
        self.rx_thread.stop()
        self.fd.close()
        transport.Transport.stop(self)
        
    def attend(self, **kw):
        '''
        Attends rx received
        '''
        raw = kw.get('raw')
        address = kw.get('address')

        self.stats['rx'] += len(kw['raw'])
        
        # pylint: disable-msg = E1101
        self.publish(what='transport/rx', raw=raw, address=address)
        
    def show_stats(self, **kw):
        '''
        Prints transmition stats
        '''
        #pylint
        dummy = kw
        
        stats = "STATS: RX: %d TX: %d Tot: %d" % (self.stats['rx'], self.stats['tx'], self.stats['rx']+self.stats['tx'])
        
        return stats


        
    
