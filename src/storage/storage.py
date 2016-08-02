#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Storage prototype
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

class Storage(tserver.TServer, zobject.ZObject):

    '''
    Hides storage intrinsics from logic.
    Decouples storage from application and ANY storage implementing
    this API wil fit.
    
    This class privides a prototype which must be implemented in derived class
    '''
    
    core = None
    
    def __init__( self, *args, **kw ):
        
        tserver.TServer.__init__(self, *args, **kw)
        zobject.ZObject.__init__(self, *args, **kw)
        
    def check_database(self, **kw):
        
        '''
        Virtual method
        '''
        
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def store_message(self, **kw):
        
        '''
        Virtual method
        '''
                
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def get_pending_messages(self, **kw):
        
        '''
        Virtual method
        '''
                
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def get_pending_contacts(self, **kw):
        
        '''
        Virtual method
        '''
        
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def new_contact(self, **kw):
        
        '''
        Virtual method
        '''
        
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def accept_contact(self, **kw):
        
        '''
        Virtual method
        '''
        
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def get_contact(self, **kw):
        
        '''
        Virtual method
        '''
        
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def get_contacts(self, which='all', **kw):
        
        '''
        Virtual method
        '''
        
        #pylint 
        dummy = kw
        dummy = which
        
        log.error("Virtual method. Must redefine")
    

    def do_ack(self, **kw):
        
        '''
        Virtual method
        '''
        
        #pylint 
        dummy = kw
        
        log.error("Virtual method. Must redefine")
    

    def remove_contact(self, email, delete_all=False, **kw):
        
        '''
        Virtual method
        '''
        
        
        #pylint 
        dummy = kw
        dummy = email
        dummy = delete_all
        
        
        log.error("Virtual method. Must redefine")
        
    def stop(self):
        
        '''
        Specific stop tasks
        '''
        
        tserver.TServer.stop(self)
    
    
        
            
            
        

        
        
        
    
    
        
