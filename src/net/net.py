#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Net module
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

# pylint: disable-msg = E1101

import threading
import time

from utils import utils
from core import tserver
from core import zobject
import udp_transport
import router
import protocol
import firewall

log = utils.log

class Net(tserver.TServer, zobject.ZObject):

    '''
    Net class
    '''
    
    HELO = 'HEL'
    SEA = 'SEA'
    DATA = 'DATA'
    CALL = 'CAL'
    ACK = 'ACK'
    
    transport = None
    protocol = None
    router = None
    presenter = None
    firewall = None

    punchers = {}
    discoverers = {}
    
    def __init__(self, *args, **kw):
        tserver.TServer.__init__(self, *args, **kw)
        zobject.ZObject.__init__(self, *args, **kw)

        self.wakeup()
        
    def wakeup(self):

        '''
        Wakeup net instance
        '''
        
        self.protocol = protocol.Zoe(core=self.core, name='ZProtocol')
                
        self.firewall = firewall.firewall(core=self.core, name='firewall')
        self.firewall.start()
        
        self.transport = udp_transport.UDPPtransport(name='transport', core=self.core)
        self.transport.start()

        self.router = router.Router(name='router', port=self.transport.fd_port, core=self.core)
        self.router.start()

        # register own in router
        # this way, two nodes can connect if one of them is a valid presenter
        
        data = {}
        data['ips'] = utils.Net_Utils.get_ips()
        data['port'] = self.transport.fd_port
        self.router.update(self.core.my_id, (data['ips'][0], self.transport.fd_port), info=data, volatile=False )
                
        
        # Consider:
        # If there is no presenter set assume we ARE a pure presenter and
        # dont keep refreshing peers
        self.presenter = self.core.configManager.get('General', 'presenter')
        if self.presenter:
            ip, port = self.presenter.split(':')
            self.router.update('presenter', (ip, int(port)), volatile=False)
            self.timer(name='publish_net', timer=10,  method=self.publish_net) 

        self.subscribe('transport/rx/*', self.attend_rx)
        
    
    def search(self, who, **kw):

        '''
        Tells all its known peers we are looking for who
        '''

        #pylint
        dummy = kw
        
        if self.discoverers.get(who):
            log.info("There is allready one discoverer looking for %s" % who )
            return
  
        # launch a little thread for searching for a while
  
        discover = Discover(net=self, remote=who)
        
        self.discoverers[who] = discover
        
        discover.start()
        
        
    def publish_net(self, **kw):

        '''
        Refresh own coordenates at known remotes
        '''

        #pylint
        dummy = kw
        
        data = {}
        data['ips'] = utils.Net_Utils.get_ips()
        data['port'] = self.transport.fd_port
        
        for to in self.router.remotes.keys():
            
            if to == self.core.my_id:
                continue # dont publish to ourselve !!
            
            address = self.router.get_address(to)
            if address:
                self._send_hello(to, address)
            
    def _send_hello(self, target, address):

        '''
        Sends hello message to remote
        '''
        
        data = {}
        cmd = Net.HELO
        data['ips'] = utils.Net_Utils.get_ips()
        data['port'] = self.transport.fd_port
        
        msg = self.protocol.encode(to=target, cmd=cmd, payload=data)
        self.transport.send(msg, address)
        
    def stop(self):
        '''
        stops net instance
        '''
        tserver.TServer.stop(self)
        self.firewall.stop()
        self.transport.stop()
        self.router.stop()
        dummy = 1
        
    def attend_rx(self, **kw):
        '''
        Public attend rx method
        '''
        self.activity(wait=120, method=self._attend_rx, **kw)
        
    def _attend_rx(self, **kw):

        '''
        Private attend method 
        '''
        
        raw = kw.get('raw')
        msg = self.protocol.decode(raw)
        
        if not self.firewall.allow_in(**msg):
            log.info("incomming msg rejected by firewall")
            return False
        
        sender = msg['from']
        address = kw['address']
        info = msg['payload']
        cmd = msg['cmd']
        
        msg['address'] = address

        if cmd != Net.HELO:
            self.router.update(sender, address)
        
        if cmd == Net.HELO:
            self.router.update(sender, address, info=info)
        elif cmd == Net.SEA:
            self._do_search(caller=sender, called=info['who'])
        elif cmd == Net.DATA:
            self._do_data(**msg)
        elif cmd == Net.CALL:
            self._do_call(**msg)
        elif cmd == Net.ACK:
            log.info("Recibido ACK de %s [%s]" % (msg['from'], msg['mid']))
            self._do_ack(**msg)
        else:
            pass

    def _do_data(self, **msg):

        '''
        Method called then DATA is received
        '''
        
        # Encrypted ??
        if msg.get('signature'):
            plain = utils.RSA(config=self.core.configManager).decrypt(msg['payload'], msg['from'], msg['signature'])
            if not plain:
                log.warning("Unencrypt failed !!")
                return
            else:
                msg['payload'] = plain
        
        
        storage = self.core.storage
        sql = "select ackd from messages where id = '%s'" % msg['mid']
        
        response, _ = storage.wait_activity(wait=10, method=storage.execute, sql=sql)
        
        if response and len(response['rows']) == 0:
            # mensaje nuevo
            # pylint: disable-msg = E1101
            self.publish(what='net/new_message', msg=msg)
        else:
            # duplicated
            pass
        
        if msg.get('msg_type') == 'INV':
            
            msg['rxtx'] = 'rx'
            msg['email'] = msg['from']
            
            email = msg['email']
            
            contacts = self.core.contacts
            result, _ = contacts.wait_activity(wait=10, method=contacts.new_contact, **msg)
            if not result:
                log.error("Error registering new contact")
                return
            
            log.info("New invitation received from %s" % email)
        
            autoaccept = self.core.configManager.get('Contacts', 'autoaccept') or False 
            if autoaccept in ['Yes', 'yes', 'Y', 'y', 'True', 'true',]:
                log.info("Autoaccepting contact %s. Check config for disable" % email)
                self.core.node.activity(method=self.core.node.accept_contact, email=email)
                
        elif msg.get('msg_type') == 'ACP':
            
            contacts = self.core.contacts
            contacts.activity(wait=100, method=contacts.accept_contact, email=msg['from'])
            
        else:
            pass
        
        # ACK is always sent as remote could loss previous
        self._send_ack(**msg)
        
    def _do_ack(self, **msg):
        '''
        Private method called when ack is received
        '''
        # pylint: disable-msg = E1101
        mid = msg.get('payload').get('mid')
        self.publish(what='net/ack/%s' % mid)
        
    def _send_ack(self, **kw):
        '''
        Sends ack for a received message
        '''
        cmd = Net.ACK
        data = {}
        data['mid'] = kw['mid']
        
        msg = self.protocol.encode(to=kw['from'], cmd=cmd, payload=data)
        self.transport.send(msg, kw['address'])
        
    def _do_call(self, **msg):

        '''
        Method called when CAL message is received.
        Sends HEL to remote
        '''
                
        info = msg['payload']
        
        who = info.get('from')

        log.info("CALL received from %s for %s" % (msg['from'], info['from']))
                
        if self.punchers.get(who):
            log.info("There is allready one Puncher against %s" % who )
            return
                
        info['net'] = self
        puncher = Puncher(**info)

        self.punchers[who] = puncher

        puncher.start()
        
            
    def _do_search(self, caller, called):

        '''
        Presenter feature: when SEA is received, check if knows both
        peers and send both message CAL
        '''

        node_a = self.router.remotes.get(caller)
        node_b = self.router.remotes.get(called)
        
        log.info("Received SEARCH from %s to %s" % (caller, called))
                
        if node_a and node_b:
            
            # send CAL to b
            info = node_a.get('info')
            info['from'] = caller
            info['address'] = node_a.get('address')
            b_address = self.router.get_address(called)
            if info and b_address:
                msg = self.protocol.encode(to=called, cmd=Net.CALL, payload=info)
                self.transport.send(msg, b_address)

            # send CAL to a
            info = node_b.get('info')
            info['from'] = called
            info['address'] = node_b.get('address')
            a_address = self.router.get_address(caller)
            if info and a_address:
                msg = self.protocol.encode(to=caller, cmd=Net.CALL, payload=info)
                self.transport.send(msg, a_address)
        
        
    def send(self, to, msg, **kw):
        '''
        Public send method
        '''
        self.activity(wait=120, method=self._send, to=to, msg=msg, **kw)
        
        
    def _send(self, to, msg, **kw):
        '''
        Private send method
        '''
        
        address = self.router.get_address(to)
        if not address:
            #self.search(to)
            pass
        else:
            cmd = kw.get('cmd', 'DATA')
            
            if kw.get('encrypt'):
                try:
                    msg, signature = utils.RSA(config=self.core.configManager).encrypt(msg, to)
                    kw['signature'] = signature
                except Exception, why:
                    log.error("OOps !! could not encrypt message %s" % why)
                    return
            
            msg = self.protocol.encode(to=to, payload=msg, cmd=cmd, **kw)
            self.transport.send(msg, address)
            
            
class Discover(threading.Thread):
    '''
    launches discover for a while
    '''

    remote = None
    
    def __init__(self, **kw):
        threading.Thread.__init__(self)
        
        self.remote = kw.get('remote')
        self.net = kw.get('net')
        
    def run(self):
 
        log.info("Starting discover for %s" % self.remote)
        
        t = time.time()
        while time.time() -t < 10:
            
            if self.net.router.get_address(self.remote):
                break
        
            data = {}
            cmd = Net.SEA
            data['who'] = self.remote
            for to in self.net.router.remotes.keys():
                if to == self.net.core.my_id:
                    continue
                address = self.net.router.get_address(to)
                msg = self.net.protocol.encode(to=to, cmd=cmd, payload=data)
                self.net.transport.send(msg, address)
                
            time.sleep(2)
        
        self.net.discoverers.pop(self.remote)
        
        success = 'Success' if self.net.router.get_address(self.remote) else 'Fail'
        
        log.info("Ended discover for %s [%s]" % (self.remote, success))
            
class Puncher(threading.Thread):
    '''
    launches a puncher for a while
    '''

    remote = None
    ips = None
    port = None
    net = None
    
    def __init__(self, **kw):
        threading.Thread.__init__(self)

        self.seen_address = kw['address']
        self.remote = kw.get('from')
        self.ips = kw.get('ips')
        self.port = kw.get('port')

        self.net = kw.get('net')
        
    def run(self):
 
        log.info("Starting Puncher for %s" % self.remote)
        
        t = time.time()
        while time.time() -t < 10:
            
            if self.net.router.get_address(self.remote):
                break

            for ip in self.ips:
                address = (ip, self.port)
                self.net._send_hello(self.remote, address)
                
            self.net._send_hello(self.remote, self.seen_address)    
                
            time.sleep(1)
            
        success = 'Success' if self.net.router.get_address(self.remote) else 'Fail'
        
        self.net.punchers.pop(self.remote)
        
        log.info("Ended Puncher for %s [%s]" % (self.remote, success))
            
        
        
    
