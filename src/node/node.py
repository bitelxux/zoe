#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Node module
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

class Node(tserver.TServer, zobject.ZObject):


    '''
    Node class
    '''
    
    semaphore = False
    
    core = None
    name = None
    
    def __init__(self, *args, **kw):

        tserver.TServer.__init__(self, *args, **kw)
        zobject.ZObject.__init__(self, *args, **kw)
       
        # Timers
        # pylint: disable-msg = E1101
        self.timer(name='process_pending', timer=30, method=self._process_pending)
        self.timer(name='discover', timer=30, method=self.discover)
        
        # Subscriptions
        self.subscribe('net/ack/*', self._do_ack)    
        self.subscribe('net/new_message/*', self._do_new_message)    
        self.subscribe('router/new_peer/*', self._process_pending)
        
    def _process_pending(self, **kw):

        '''
        Tries to deliver pending messages
        '''
        
        #pylint
        dummy = kw
        
        storage = self.core.storage

        # pylint: disable-msg = E1101
        result, _ = storage.wait_activity(wait=100, method=storage.get_pending_messages)
        
        rows = result['rows'] if result else []
            
        for message in rows:
            self.core.net.send(message['recipient'], 
                               message['payload'], 
                               mid=message['id'], 
                               encrypt=message['encrypt'],
                               msg_type=message['type'])
            
 
    def discover(self, **kw):

        '''
        Tries lo locate contacts addresses with pending messages for them
        '''

        #pylint
        dummy = kw
         
        net = self.core.net
       
        storage = self.core.storage
        
        result, _ = storage.wait_activity(wait=100, method=storage.get_pending_contacts)
        
        rows = result['rows'] if result else []
            
        for row in rows:
            if not row['recipient'] in net.router.remotes:
                net.activity(wait=100, method=net.search, who=row['recipient'])
            
        
    def _do_ack(self, **kw):

        '''
        Update storage based on received ack
        '''

        mid = kw['what'][len('net/ack/'):]
        
        #TODO: use regular

        storage = self.core.storage
        storage.activity(wait=100, method=storage.do_ack, mid=mid)

    def _do_new_message(self, **kw):
      
        '''
        Reacts to new received message
        '''

        msg = kw['msg']        
        
        # reject not accepted contacts
        if msg.get('msg_type') not in ['INV', 'ACP']:
            contacts = self.core.contacts
            contact = contacts.get_contact(email=msg.get('from'))
            if not contact or not contact.get('ackd'):
                log.info("Rejected msg from not authorized contact %s" % kw.get('from'))
                return
        
        storage = self.core.storage
        
        data = {}
        data['id'] = msg['mid']
        data['payload'] = msg['payload']
        data['ts'] = time.time()
        data['sender'] = msg['from']
        data['recipient'] = msg['to']
        data['msg_type'] = msg['msg_type']
        data['meta'] = msg.get('meta')
        data['encrypt'] = msg.get('encrypt', 0)
        
        storage.activity(wait=100, method=storage.store_message, msg=data)
        
        log.info("New message from %s: %s" % (msg['from'], msg['payload']))
        
        echo = self.core.configManager.get('Messages', 'echo') or False 
        
        if echo and msg.get('msg_type') == 'TXT':
            # if echo is set in config, echo message back to sender
            if echo in ['Yes', 'yes', 'Y', 'y', 'True', 'true',]:
                log.info("Echoing message. Check config for disable.")
                self.new_message(msg['from'], "ECHO: %s" % msg['payload'])
        
        
    def new_message(self, recipient, body, **kw):

        '''
        On new generated message, stores it on storage
        '''

        #pylint
        dummy = kw
  

        # Only invitations and acceptations can be sent to not contacts
        if kw.get('msg_type') not in ['INV', 'ACP']:
            
            contacts = self.core.contacts
            contact = contacts.get_contact(email=recipient)
        
            if not contact or not contact.get('ackd'):
                text = "Can't send to not contact or not accepted contact %s" % recipient
                log.warning(text)
                print text
                return False, text
          
        data = {}
        data['id'] = utils.hex_uuid()
        data['payload'] = body
        data['ts'] = time.time()
        data['sender'] = self.core.my_id
        data['recipient'] = recipient
        data['msg_type'] = kw.get('msg_type', 'TXT')
        data['encrypt'] = kw.get('encrypt', 0)
        data['meta'] = None
        
        storage = self.core.storage

        # pylint: disable-msg = E1101
        result, _ = storage.wait_activity(method=storage.store_message, msg=data)
        self.activity(wait=10, method=self._process_pending)
        
        if result:
            return True, "Message enqueued for delivering"
        else:
            return False, "Error enqueueing message"
        
        
    def invite_contact(self, email, **kw):

        '''
        On new contact, stores it on storage
        '''

        contacts = self.core.contacts
        result = contacts.get_contact(email=email)
        if result:
            log.info("Node: Allready known contact !! %s" % email)
            return None, "Allready known contact %s!!" % email
        
        kw['rxtx'] = 'tx' # Invitation sent
        
        contacts = self.core.contacts
        
        kw.setdefault('wait', 10)
        result, _ = contacts.wait_activity(method=contacts.new_contact, email=email, **kw)
        
        # generate INV message
        # When this message is ackd, remote does has the invitation
        # and its not sent again unless force
        
        text = kw.get('text', "Hi !! I want you to be my contact !!")
        msg_type = 'INV'

        mid = self.new_message(email, msg_type=msg_type, body=text)
        
        return result, "Invitation enqueued to %s [%s]" % (email, mid)
        

    def accept_contact(self, email, **kw):

        '''
        Accepts invitation
        '''

        contacts = self.core.contacts
        
        contact = contacts.get_contact(email=email)
        if contact.get('ackd'):
            log.info("Contact %s is allready accepted" % email)
            return False, "Contact %s is allready accepted" % email
        
        if contact.get('rxtx') == 'tx':
            log.info("Oops, you can't accept in %s's name !!" % email)
            return False, "Oops, you can't accept in %s's name !!" % email
        
        kw.setdefault('wait', 10)
        result, _ = contacts.wait_activity(method=contacts.accept_contact, email=email, **kw)
        if not result:
            log.error("Error accepting contact %s" % email)
            return False, "Error accepting contact %s" % email
        
        # generate ACP -accept- message
        # When this message is ackd, remote does has the invitation
        # and its not sent again unless force
        
        text = kw.get('text', "Contact invitation accepted !!")
        msg_type = 'ACP'

        result = self.new_message(email, msg_type=msg_type, body=text)
        
        return True, "Contact %s accepted" % email
    
    def delete_contact(self, email, delete_all=False, **kw):

        '''
        removes contacts
        '''

        contacts = self.core.contacts
        
        contact = contacts.get_contact(email=email)
        if not contact:
            return False, "Contact %s doesn't exists" % email

        kw.setdefault('wait', 10)
        result, _ = contacts.wait_activity(method=contacts.remove_contact, email=email, delete_all=delete_all, **kw)
        
        if not result:
            log.error("Error deleting contact %s" % email)
            return False, "Error deleting contact %s" % email
        
        return True, "Contact %s deleted" % email

    def get_contacts(self, **kw):

        '''
        get contacts list
        '''

        storage = self.core.storage
        
        kw.setdefault('wait', 10)
        result, _ = storage.wait_activity(method=storage.get_contacts, **kw)
     
        return result
    
    
    def get_message(self, which='all', **kw):

        '''
        delete message
        '''

        storage = self.core.storage
        
        kw.setdefault('wait', 10)
        result, _ = storage.wait_activity(method=storage.get_message, mid=which)
     
        return result
    
    def delete_message(self, mid, **kw):

        '''
        delete message
        '''

        storage = self.core.storage
        
        kw.setdefault('wait', 10)
        result, _ = storage.wait_activity(method=storage.get_message, mid=mid)
        
        
        if not result:
            return False, "Message %s doesn't exists" % mid

        kw.setdefault('wait', 10)
        result, _ = storage.wait_activity(method=storage.delete_message, mid=mid, **kw)
        
        if not result:
            log.error("Error deleting message %s" % mid)
            return False, "Error deleting message %s" % mid
        
        return True, "Message %s deleted" % mid
     
    
    def mark_message(self, **kw):
        
        '''
        marks message as read or unread
        '''

        storage = self.core.storage
        
        kw.setdefault('wait', 10)
        result, _ = storage.wait_activity(method=storage.mark_message, **kw)
        
        if not result:
            log.error("Error setting message %s" % kw.get('mid'))
            return False, "Error setting message %s" % kw.get('mid')
        
        return True, "Message marked as %s" % kw.get('mark')
        
        
        
        
        
        
        
        
    
