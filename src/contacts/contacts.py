#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Contacts funcionality
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

# pylint: disable-msg = R0903
class Contacts(tserver.TServer, zobject.ZObject):

    '''
    Contacts class
    '''

    core = None
    name = None
    
    def __init__(self, *args, **kw):
        
        tserver.TServer.__init__(self, *args, **kw)
        zobject.ZObject.__init__(self, *args, **kw)
        
    def new_contact(self, **contact):
        
        '''
        Adds new received or invited contact
        '''
        
        storage = self.core.storage
        
        email = contact['email']
        
        result = self.get_contact(email=email)
        if result :
            log.info("Contacts: Allready known contact !! %s" % email)
            return None
                                              
        result, _ = storage.wait_activity(method=storage.new_contact, **contact)
        
        # pylint: disable-msg = E1101    
        self.publish(what='contacts/new_contact', **contact)
 

        return result
    
    def accept_contact(self, email, **kw):
        
        '''
        Accepts invitation
        '''

        result = self.get_contact(email=email)
        if result.get('ackd'):
            log.info("Contacts: Allready accepted contact %s!!" % email)
            return None
                
        storage = self.core.storage
        result, _ = storage.wait_activity(method=storage.accept_contact, email=email, **kw)
        
        if result:
            # pylint: disable-msg = E1101
            self.publish(what='contacts/accepted', email=email)
            log.info("%s accepted invitation" % email)
        
        return result
    
    def get_contact(self, **kw):

        '''
        get contact
        '''

        storage = self.core.storage
        contact, _ = storage.wait_activity(method=storage.get_contact, **kw)
        
        return contact
        
    
    def get_contacts(self, which='all', **kw):
        
        '''
        get contacts
        '''
        
        storage = self.core.storage
        result, _ = storage.wait_activity(wait=30, method=storage.get_contacts, which=which, **kw)
        return result['rows'] if result else result
    
    def remove_contact(self, **kw):
        
        '''
        removes contact and all his messages
        '''
        
        storage = self.core.storage
        kw.setdefault('wait', 30)
        result, _ = storage.wait_activity(method=storage.remove_contact, **kw)
        return result
    
        
    
         

    
                
        
        
                           
        
        
        
        
        
        
        
        
    
