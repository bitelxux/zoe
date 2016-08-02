#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
sqlite_db storage module
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

import storage
import sqlite3
import time

log = utils.log

def dict_factory(cursor, row):
    '''
    Dict factory to get results as dictionary
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# pylint: disable-msg = R0903
class MyCursor(sqlite3.Cursor):
    '''
    Specialized cursor with dict row factory
    '''
    def __init__(self, *args, **kw):
        sqlite3.Cursor.__init__(self, *args, **kw)
        self.row_factory = dict_factory
        
class SqliteDB(storage.Storage):
    
    '''
    This class inherits from TServer.
    Its methods MUST be called through "activity" or "wait_activity" methods
    '''
    
    now = "datetime('now','localtime')"
    
    db = None    
    cursor = None
    
    ERROR = -99
    
    def __init__( self, *args, **kw ):
        
        storage.Storage.__init__(self, *args, **kw)        
        
        kw.setdefault('db', '%s.db' % self.core.configManager.get('General', 'id'))
        self.db = kw.get('db')

        
        # As init is called from other thread, we can't create db connection here.
        # Send a nonblocking activity to let own sqlitestorage thread to create
        # the connection
        # callback is not needed and can be removed
        # pylint: disable-msg = E1101
        self.activity(wait=5.0, method=self.connect, callback=self.connection_callback, **kw)
        #self.timer(name='purge', method=self.purge, timer=3600, skeep=1)
       
    def connection_callback(self, **kw):
        
        '''
        Called when connectin is done
        '''

        #pylint
        dummy = kw

        if kw.get('result') == 'timeout':
            log.error("Error connecting db: timeout")
            return
        
        if kw.get('result'):
            log.info('SqliteStorage connection created in %0.3f seconds' % kw.get('lapse'))
        else:
            log.error('Oops, Sqlite connection could not be created !!')
        
    def connect(self, **kw):

        '''
        Connects to database, set pragmas, get cursor and check database
        '''

        #pylint
        dummy = kw

        #db = self.check_scheme()
        self.db = sqlite3.connect(self.db, timeout=10, isolation_level='DEFERRED')
        
        self.db.execute('PRAGMA synchronous=OFF')
        self.db.execute('PRAGMA count_changes=OFF')
        self.db.execute('PRAGMA journal_mode = MEMORY')
        self.db.execute('PRAGMA page_size = 4096')
        self.db.execute('PRAGMA cache_size=5000')
        
        self.cursor = self.db.cursor(factory=MyCursor)    
        
        self.check_database()
        
        return self.db
                
    def stop(self, **kw):
        '''
        calls private stop method
        '''
        # pylint: disable-msg = E1101
        dummy = kw

        self.wait_activity(wait=60, method=self._stop)
        
    def _stop(self, **kw):
        '''
        stops connection
        '''
        #pylint
        dummy = kw

        storage.Storage.stop(self)
        self.commit()
        self.cursor.close()
        self.db.close()
        
    def commit(self, **kw):
        '''
        does pending commits
        '''
        #pylint
        dummy = kw

        try:
            self.db.commit()
        except Exception, why:
            log.warning('Could not commit !!' % why)
    
    def execute(self, **kw):

        '''
        Executes sql statement
        '''
        
        result = None
        num = self.ERROR
        
        try:
            #self.lock.acquire()
            self.cursor.execute(kw.get('sql'))
            num = self.cursor.rowcount
            result = self.cursor.fetchall()
            num = len(result) if len(result) else num
            self.commit()
        except Exception, why:
            log.warning("sqlite storage: %s" % why )
            
        return {'rows':result, 'affected':num}

    def check_database(self, **kw):

        '''
        Checks data base existance and creates it if needed
        '''
        
        #pylint
        dummy = kw
        
        # Create table

        sql = '''
        CREATE TABLE IF NOT EXISTS contacts( 
        email  VARCHAR( 50 ) PRIMARY KEY,
        name   VARCHAR( 50 ),
        rxtx   VARCHAR( 2 ),
        about  VARCHAR(255),
        ts     BIGINT,
        ackd   BIGINT,
        avatar BLOB 
        );
        '''
        
        self.execute(sql=sql)
        
        sql = '''
        CREATE TABLE IF NOT EXISTS messages (
        id         VARCHAR(32) PRIMARY KEY,
        payload    TEXT,
        ts         BIGINT,
        ackd       BOOLEAN,
        sender     VARCHAR( 50 ),
        recipient  VARCHAR( 50 ),
        type       VARCHAR( 3 ),
        encrypt    BOOLEAN,
        meta       VARCHAR( 5 )
        );
        '''

        self.execute(sql=sql)
    
                
    def store_message(self, **kw):

        '''
        Creates new message in storage
        '''
        
        data = kw['msg']
        data.setdefault('encrypt', 0)

        payload =  data['payload']
        try:
            data['payload'] = payload.decode('utf-8')
        except:
            pass

        
        sql = """INSERT INTO messages VALUES( '%(id)s',
                                            '%(payload)s',
                                            %(ts)d,
                                            0,
                                            '%(sender)s',
                                            '%(recipient)s',
                                            '%(msg_type)s',
                                            %(encrypt)d,
                                            '%(meta)s' )""" % data
        
        result = self.execute(sql=sql)
        return result and result.get('affected') > 0
   

    def get_pending_messages(self, **kw):

        '''
        Returns all messages not ackd
        '''

        #pylint
        dummy = kw
        
        sql = "select * from messages where sender = '%s' and ackd = 0" % (self.core.my_id)
        result = self.execute(sql=sql)
        return result

    def get_pending_contacts(self, **kw):
        
        '''
        Return contacts with pending messages
        '''

        #pylint
        dummy = kw
                
        sql = "select distinct(recipient) from messages where sender = '%s' and ackd = 0" % (self.core.my_id)
        result = self.execute(sql=sql)
        return result

    
    def new_contact(self, **kw):

        '''
        Adds new contact to storage
        '''
        
        contact = dict(kw)
        contact.setdefault('about', "Hey I'm using Zoe !!")
        contact.setdefault('avatar', None)
        contact.setdefault('name', '')
        contact.setdefault('ts', time.time())
  
        sql = "INSERT INTO contacts values(\"%(email)s\",\
                                           \"%(name)s\",\
                                           \"%(rxtx)s\",\
                                           \"%(about)s\",\
                                           %(ts)d,\
                                           0,\
                                           \"%(avatar)s\")" % contact
                                           
        result = self.execute(sql=sql)
        return True if result and result['affected'] == 1 else False

    
    def accept_contact(self, **kw):
        
        '''
        Marks contact as accepted in database
        '''
        
        sql = "UPDATE contacts SET ackd = %d WHERE email = '%s'" % (time.time(), kw.get('email'))
        result = self.execute(sql=sql)
        return True if result and result['affected'] == 1 else False

    def get_contact(self, **kw):

        '''
        Returns stored contact based on name or email
        '''
        
        if kw.get('name'):
            cond = "name LIKE '%%%s%%'" % kw['name']
            
        elif kw.get('email'):
            cond = "email = '%s'" % kw['email']
            
        else:
            log.error("storage.get_contact: oops !!")
            return

        sql = "SELECT * FROM contacts WHERE %s" % cond
        result = self.execute(sql=sql)
        
        if result and result.get('affected') == 1:
            return result['rows'][0]
        else:
            return {}
        

        
    def get_contacts(self, which='all', **kw):
        
        '''
        Retrieves contacts from storage
        '''
        
        # pylint 
        dummy = kw
        
        if which == 'all':
            cond = ''
        elif which == 'accepted':
            cond = "WHERE ackd != 0"
        elif which == 'pending':
            cond = "WHERE ackd = 0"
        else:
            log.error("Wrong which condition %s" % which)
            return False
            
        sql = "SELECT * FROM contacts %s" % cond
        
        result = self.execute(sql=sql)
        return result
        
    def do_ack(self, **kw):
        
        '''
        Acks message in storage
        '''

        mid = kw['mid']
        sql = "UPDATE messages SET ackd = %d WHERE id = '%s'" % (time.time(), mid)
        return self.execute(sql=sql)      

    
    def remove_contact(self, email, delete_all=False, **kw):
        
        '''
        Unauthorizes contact if delete_all == False
        or completly deletes contact and regarded messages
        '''
        
        #pylint
        dummy = kw
        
        contact = self.get_contact(email=email)
        if not contact:
            text = "Contact %s does not exist" % email
            log.warning(text)
            print text
            return 
        
        if not delete_all:
            if not contact.get('ackd'):
                text = "%s is allready disabled" % email
                log.warning(text)
                print text
                return 
            sql = "UPDATE contacts SET ackd=0 WHERE email = '%s'" % email
            self.execute(sql=sql)
        else:
            sql = "DELETE FROM contacts WHERE email = '%s'" % email
            self.execute(sql=sql)
            sql = "DELETE FROM messages WHERE recipient = '%s' OR sender = '%s'" % (email, email)
            self.execute(sql=sql)
            
        return True
  
    def get_message(self, mid, **kw):

        '''
        returns stored message
        '''
        
        #pylint
        dummy = kw
        
        if mid != 'all':
            sql = "SELECT * FROM messages WHERE id = '%s'" % mid
        else:
            sql = "SELECT * FROM messages WHERE type = 'TXT'"
            
        result = self.execute(sql=sql)
        
        if result and result.get('affected') == 1:
            return result['rows'][0]
        elif result:
            return result['rows']
        else:
            return {}
      
    
    def delete_message(self, mid, **kw):
        
        '''
        deletes message from storage
        '''
        
        #pylint
        dummy = kw
        
        msg = self.get_message(mid=mid)
        if not msg:
            text = "message %s does not exist" % mid
            log.warning(text)
            print text
            return 
        
        sql = "DELETE FROM messages WHERE id = '%s'" % mid
        self.execute(sql=sql)
            
        return True
    
    def mark_message(self, **kw):
        
        '''
        Marks message as read or unread
        read -> current timestamp
        unread -> 0
        '''

        mark = time.time() if kw.get('mark') == 'read' else 0
        
        mid = kw['mid']
        sql = "UPDATE messages SET ackd = %d WHERE id = '%s'" % (mark, mid)
        result = self.execute(sql=sql)
        
        return result
    
    
    
    
