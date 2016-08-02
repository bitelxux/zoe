# -*- coding: utf-8  -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Zoe console extension
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

import re
import time

from utils import utils
import console

log = utils.log

# compiled regulars. just for performance

reg_sample = re.compile(r"(?P<cmd>sample)", re.DOTALL | re.MULTILINE)
reg_sql = re.compile(r"(?P<cmd>sql) (?P<query>.*)", re.DOTALL | re.MULTILINE)
reg_uptime = re.compile(r"(?P<cmd>uptime)", re.DOTALL | re.MULTILINE)
reg_contact = re.compile(r"(?P<cmd>contact) (?P<action>\w+)( (?P<contact>.*))?", re.DOTALL | re.MULTILINE)
reg_message = re.compile(r"(?P<cmd>msg|cmsg) (?P<action>send|read|unread|delete|del|history)( (?P<crypted>(crypted)))?( (?P<p1>(\w|@|\.)+))?( (?P<p2>.*))?", re.DOTALL | re.MULTILINE)
reg_group = re.compile(r"(?P<cmd>group) (?P<action>\w+)( (?P<params>.*))?", re.DOTALL | re.MULTILINE)

class zoe_console( console.TelnetConsole ):

    '''
    zoe console
    '''
    
    local_helpers = {}
    
    def __init__(self, *args, **kw):
        
        console.TelnetConsole.__init__( self, *args, **kw )
                
        self.local_helpers = { 
            'sample':{'reg':reg_sample, 'func':self.helper_sample, 'info':'Helper sample', 'help':self.help_sample},
            'sql':{'reg':reg_sql, 'func':self.helper_sql, 'info':'Sql wrapper', 'help':self.help_sql},
            'contact':{'reg':reg_contact, 'func':self.helper_contacts, 'info':'Manage contacts', 'help':self.help_contacts},
            'msg':{'reg':reg_message, 'func':self.helper_messages, 'info':'Manage messages', 'help':self.help_messages},
            
        }
        
        for command, data in self.local_helpers.items():
            self.doc[command] = data['help']
        
        self.public_commands.extend(['sample',])

        self.helpers.update(self.local_helpers)


    def help_sample(self):
        
        '''
        shows sample help
        '''
        
        self.write("")
        self.write("sample")
        self.write("")
        self.write("Does nothing. It's just a sample command")
        
        
    def help_sql(self):
        
        '''
        shows sql help
        '''
        
        self.write("")
        self.write("sql <sql sentence>")
        self.write("")
        self.write("Executes sql sencente")
        
        
    def help_contacts(self):
        '''
        contacts management help
        '''
        
        self.write("")

        self.write("Show contacts: contact show")        
        self.write("Invite contact: contact invite <email>")
        self.write("Accept contact: contact accept <email>")
        self.write("Delete contact: contact delete <email> [all]")
        self.write("\t[all] deletes all contact messages too")

    def help_messages(self):
        '''
        messages management help
        '''
        
        self.write("")
        self.write("send [encrypt] <to> <body>")
        self.write("")
        self.write("\t[encrypt] forces message to be encrypted with to's public key")
        self.write("")
        self.write("examples")
        self.write("")
        self.write("send jhon@gmail.com Hi !! what's up !!??")
        self.write("")
        self.write("\tsends plain message to jhon")
        self.write("")
        self.write("send crypted jhon@gmail.com Hi !! what's up !!??")
        self.write("")
        self.write("\tsends RSA crypted message to jhon")
        self.write("")
        self.write("\t* We need to have public jhon's key")
        self.write("\t* Jhon needs to have our public key")
        
                
    def help_groups(self):
        '''
        groups management help
        '''
        
        self.write("")
        
        self.write("")
        self.write("")
        self.write("")
        self.write("")
            
    def helper_contacts(self, **kw):
        '''
        helper contact actions
        '''
            
        node = self.core.node
        
        action = kw.get('action')

        if action not in ['invite', 'accept', 'delete', 'help', 'show']:
            self.write("Unknown contact command [%s]" % action)
            self.help_contacts()
            return
        
        if action not in ['help', 'show', ]:
            
            params = kw.get('contact').split(' ')
            contact = params[0]
            options = None
        
            if len(params) > 1:
                options = params[1]
        
        if action == 'show':
            result, _ = node.wait_activity(wait=30, method=node.get_contacts)
            contacts = result['rows'] if result else []
            if result:
                result = ('OK', '%d contacts' % len(contacts))
            for contact in contacts:
                state = 'confirmed' if contact.get('ackd') else 'pending'
                self.write('[%s] %s' %(state, contact.get('email')))
        elif action == 'invite':
            result, _ = node.wait_activity(wait=30, method=node.invite_contact, email=contact)
        elif action == 'accept':
            result, _ = node.wait_activity(wait=30, method=node.accept_contact, email=contact)
        elif action == 'delete':
            delete_all = True if options == 'all' else False
            result, _ = node.wait_activity(wait=30, method=node.delete_contact, email=contact, delete_all=delete_all)
        elif action == 'help':
            self.help_contacts()
            return
        else:
            self.write("Wrong contact action [%s]" % action)
            return
            
        if not result[0]:
            self.write("Error: %s" % result[1])
        else:
            self.write("OK: %s" % result[1])
            

    def helper_groups(self, **kw):
        '''
        helper group actions
        '''
        
        action = kw.get('action')
        
        if action == 'create':
            self.write("Sorry, not implemented.")
        elif action == 'delete':
            self.write("Sorry, not implemented.")
        elif action == 'addcontact':
            self.write("Sorry, not implemented.")
        elif action == 'delcontact':
            self.write("Sorry, not implemented.")
        elif action == 'help':
            self.write("Sorry, not implemented.")
        else:
            self.write("Wrong group action")
            
    # pylint: disable-msg = R0914        
    def helper_messages(self, **kw):
        '''
        helper messages actions
        '''
        
        my_id = self.core.my_id
        
        node = self.core.node
        
        action = kw.get('action')
        encrypt = False
        
        if action == 'send':
            encrypt = True if kw.get('crypted') == 'crypted' else False
            to = kw.get('p1')
            body = kw.get('p2')
            result, _ = node.wait_activity(method=node.new_message, recipient=to, body=body, encrypt=encrypt)
            
        elif action in ['del', 'delete',]:
            mid = kw.get('p1')
            result, _ = node.wait_activity(method=node.delete_message, mid=mid)
            
        elif action == 'read':
            msg_id = kw.get('p1')
            result, _ = node.wait_activity(method=node.mark_message, mid=msg_id, mark='read')
            
        elif action == 'unread':
            msg_id = kw.get('p1')
            result, _ = node.wait_activity(method=node.mark_message, mid=msg_id, mark='unread')  
            
        elif action == 'history':
            result, _ = node.wait_activity(method=node.get_message, which='all')  
            if result:
                for m in result:
                    
                    mid = m['id']
                    fecha = utils.timestamp_2string(m['ts'])
                    _from = m['sender']
                    _to = m['recipient']
                    
                    if m.get('from') == my_id and m.get('ackd'):
                        done = 'done'
                    elif m.get('from') != my_id:
                        done = 'done'
                    else:
                        done = 'pending'
                        
                    body = m['payload']
                    
                    msg = "%s %s from:%s to:%s [%s] body:%s" % (fecha, mid, _from, _to, done, body)
                    self.write(msg)
                    
            result = ("OK", "%d messages" % len(result))
                    
        elif action == 'help':
            dummy = 1
            
        else:
            self.write("Wrong group action")
            
        if not result[0]:
            self.write("Error: %s" % result[1])
        else:
            self.write("OK: %s" % result[1])
            
        
    def do_helper(self, helper, **kw):
        '''
        Executes console action
        '''
        
        if self.logged is False and kw.get('cmd') not in self.public_commands:
            self.write('oops !! Not logged !!')
        else:
            try:
                helper(**kw)
            except Exception, why:
                self.write("Error: %s" % why )        
        
    def helper_info(self, **kw):
        uptime = utils.dhms_time(time.time() - self.core.started_at)
        build = self.core.BUILD
        
        self.write("Build: %s" % build)
        self.write("Uptime: %s" % uptime)
                
    def helper_sample(self, **kw):
        '''
        helper sample
        '''
        dummy = kw
        self.write("this is a sample")

    def helper_uptime(self, **kw):
        
        uptime = time.time() - self.core.started_at
        self.write("Uptime: %s" % utils.dhms_time(uptime))
        
    def helper_sql(self, **kw):
        '''
        SQL storage wrapper
        '''
        storage = self.core.storage
        query = kw.get('query')
        result, lapse = storage.wait_activity(wait=15.0, method=storage.execute, sql=query) 
        
        if result is None:
            self.write('Time out')
        elif result.__class__.__name__ == 'OperationalError':
            self.write("Error: %s" % result)
        else:
            for record in result['rows']:
                #text = '(' + ', '.join("'%s'" %str(value) for value in record) + ')' 
                self.write('%s' % record)
            self.write('%d tuples in %0.3f seconds' %(result['affected'], lapse))
                
    def helper_stop(self, **kw):
        self.write('Stopping App')
        self.core.stop()
        
        

