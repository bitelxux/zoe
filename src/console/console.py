# -*- coding: utf-8  -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Console funcionality
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

import code
import sys
import StringIO
import re
import time

import socket
import select

import utils

from utils import utils
log = utils.log

class myInteractiveInterpreter( code.InteractiveInterpreter ):
    '''
    Python Console
    '''

    def __init__(self, _write, locals=None):
        if locals is None:
            locals = {}
        code.InteractiveInterpreter.__init__( self, locals )
        self._write = _write

    def runcode(self, _code):
        _buffer = StringIO.StringIO( )
        sys.stdout = _buffer
        try:
            code.InteractiveInterpreter.runcode( self, _code )
        finally:
            sys.stdout = sys.__stdout__
        _buffer.seek( 0 )
        map( self.write, _buffer.readlines( ) )

    def write(self, data):
        self._write( data.replace( '\n^', '^' ).replace( '\n', '\r\n' ) )

# Uncompiled regulars

# login. "login <user>:<passwd>" ej login bitlx.novo@gmail.com:abracadabra
r_email = "(?P<user>[-A-Z-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6})"
r_passwd = "(?P<pass>.*)"
r_login = "(?P<cmd>login)\s%s" % (r_passwd)

# compiled regulars. just for performance

reg_login = re.compile(r"%s" % r_login, re.DOTALL | re.MULTILINE)
reg_cmd = re.compile(r"(?P<cmd>\w+)\s*(?P<rest>\w.*)*", re.DOTALL | re.MULTILINE)
reg_help = re.compile(r"(?P<cmd>help)( (?P<what>.*))?", re.DOTALL | re.MULTILINE)
reg_stop = re.compile(r"(?P<cmd>stop)", re.DOTALL | re.MULTILINE)
reg_quit = re.compile(r"(?P<cmd>quit)", re.DOTALL | re.MULTILINE)
reg_reset = re.compile(r"(?P<cmd>reset\s*(?P<what>.*))", re.DOTALL | re.MULTILINE)
reg_reboot = re.compile(r"(?P<cmd>reboot)", re.DOTALL | re.MULTILINE)
reg_uptime = re.compile(r"(?P<cmd>uptime)", re.DOTALL | re.MULTILINE)
reg_info = re.compile(r"(?P<cmd>info)", re.DOTALL | re.MULTILINE)

class Console(utils.ZThread):
    '''
    console
    '''

    start_time = time.time()
    
    helpers = {}
    running = False
    interpreter = None
    ok = False
    locked = True
    
    logged = False
    uptime = None
    
    doc = {}
    
    public_commands = []
    
    # pylint
    core = None

    def __init__(self, *args, **kw):

        self.is_ok = True
        self.start_time = time.time()
        utils.ZThread.__init__(self, *args, **kw)

        self.public_commands = ['login', 'uptime', 'help', 'quit', 'info']

        self.helpers = {  'login':{'reg':reg_login, 'func':self.helper_login, 'info':'User login', 'help':self.login_help},
                          'stop':{'reg':reg_stop, 'func':self.helper_stop, 'info':'Stops node', 'help':self.stop_help},
                          'quit':{'reg':reg_quit, 'func':self.helper_quit, 'info':'Quit this console', 'help':self.quit_help},
                          'help':{'reg':reg_help, 'func':self.helper_help, 'info':'Print this help', 'help':self.help_help},
                          'info':{'reg':reg_info, 'func':self.helper_info, 'info':'Shows info', 'help':self.info_help},                          
                       }

        for command, data in self.helpers.items():
            self.doc[command] = data['help']

        self.interpreter = myInteractiveInterpreter(self.write, locals=locals())

        
    def info_help(self):
        
        '''
        Shows info help
        '''
        
        help_lines = [
            "info",
            "",
            "Shows some stats about ejetution."
            ]
        
        
        self.write("")
        for line in help_lines:
            self.write(line)
        
        
    def quit_help(self):
        
        '''
        Shows quit help
        '''
        
        help_lines = [
            "quit",
            "",
            "Quits console and returns to prompt."
            ]
        
        
        self.write("")
        for line in help_lines:
            self.write(line)
        
        
    def help_help(self):
        
        '''
        Shows help help
        '''
        
        help_lines = [
            "help [command]",
            "",
            "Shows available commands."
            ]
        
        
        self.write("")
        for line in help_lines:
            self.write(line)
        
        
    def stop_help(self):
        
        '''
        Shows stop help
        '''
        
        help_lines = [
            "stop",
            "",
            "Stops node execution."
            ]
        
        self.write("")
        for line in help_lines:
            self.write(line)
        
        
    def login_help(self):
        
        '''
        Shows login help
        '''
        
        help_lines = [
            "login <password>",
            "",
            "Enables all console funcionality to user."
            ]
        
        
        self.write("")
        for line in help_lines:
            self.write(line)
        
    def unlock_python(self):
        '''
        Brings access to python console
        '''
        self.write('Great !! Python console unlocked !! You are wellcome !!')
        self.locked = False

    def lock_python(self):
        '''
        Locks python console
        '''
        self.write('Python console locked !!')
        self.locked = True

    def is_ready(self):
        '''
        Return if console is ready
        '''
        return self.is_ok

    def run(self):
        '''
        Thread loop
        '''

        self.running = True
        while self.running:
            
            utils.ZThread.run(self)
            
            #log.info("Console running")
            # pylint: disable-msg = E1101
            line = self.read('%s@>>' % self.name)
            if line == '':
                continue
            try:
                self.attend(line)
            except Exception, why:
                log.error("Oops: %s" % why )

        #print "Have a nice day. Bye"
        log.info("Console stopped")

    def firewall_allows(self, line):

        '''
        Very simple console firewall for avoiding very bad things
        '''

        forbidden = ['import os',
                     'from os import',
                     'os.system(' ]

        for bad in forbidden:
            if bad in line:
                return False

        return True

    ##########################################################################
    # >> helpers
    ##########################################################################

    #Don't call directly !! when helper is reached, regular has allready been validated ...
    #REVIEW: check regular again ?? or just call helper and check regular just in helper and not before

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

        
    def helper_uptime(self, **kw):
        '''
        helper
        '''
        #pylint 
        dummy = kw

        self.write(utils.dhms_time(time.time() - self.start_time))
        
    def helper_info(self, **kw):
        '''
        helper
        '''
        #pylint 
        dummy = kw

        self.write( "Overwrite !")
                
    def helper_reset(self, **kw):
        '''
        helper
        '''
        #pylint 
        dummy = kw
        
        self.write( "Overwrite !")
        
    def helper_reboot(self, **kw):
        '''
        helper
        '''
        #pylint 
        dummy = kw

        self.write( "Overwrite!")
        
    def helper_stop(self, **kw):
        '''
        helper
        '''
        #pylint 
        dummy = kw
        
        self.write( "Overwrite !")
                
    def helper_quit(self, **kw):
        '''
        Quits console
        '''
        assert kw['cmd'] in ('quit')
        self.write('Good bye. Have a nice day !!')
        self.close_client()

    def helper_login(self, **kw):
        '''
        User login
        '''
        assert kw['cmd'] == 'login'
        if kw.get('pass') == self.core.configManager.get('General', 'password'):
            self.logged = True
            self.write("You are now logged !! Enjoy !!")
        else:
            self.print_help()
            self.write("Oops ... login failed ... you can't use the console")


    def helper_help(self, **kw):
        '''
        Shows help
        '''
        assert kw['cmd'] == 'help'
        if not kw.get('what'):
            self.print_help()
        else:
            what = kw.get('what')
            if not self.doc.get(what):
                self.write("Oops I don't have any doc for %s !!" % what )
                self.write("")
                return
            else:
                self.doc[what]()
                self.write("")

    ##########################################################################
    # << helpers
    ##########################################################################

    def close_client(self):
        '''
        Virtual method. Must be overwritten
        '''
        self.write('This method must be overwritten !!')

    def attend(self, line):
        '''
        Main console entry point. Attends commands
        '''

        # secret word for unlocking python iteractive ??
        # 'unlock python console for me, please'
        if utils.sha1(line) == 'c64597d8a4cc46d02aa1cac5470874ebc9c50e3e':
            self.unlock_python()
            return
        # 'lock python console, please'
        elif utils.sha1(line) == 'f71897dcb339d5b12ef292ae3c1da56d77885b86':
            self.lock_python()
            return

        cmd = None

        # first: is a helper command ?
        parsed = reg_cmd.match(line)

        if parsed:
            cmd = parsed.groupdict()['cmd']

        if cmd is not None and cmd in self.helpers.keys():
            reg = self.helpers[cmd]['reg']
            parsed = reg.match(line)
            if parsed:
                
                self.do_helper(self.helpers[cmd]['func'], **parsed.groupdict())
                return
            else:
                self.write('Incorrect sintax. Please, refer to help')
                return

        if not self.firewall_allows(line):
            self.write('Bad idea, man ...')
            return

        else:

            if self.locked is True:
                self.write('Unkown command')
            else:
                # when single var is written, ej a, interpreter doesn't print it's value.
                # prefix with "print" to have normal python console behaviour
                # TODO: this is no much robust ... it's a big shit ... improve
                if '=' not in line and '<' not in line and '>' not in line and len(line.split()) == 1:
                    line = 'print %s' % line

                self.interpreter.runcode(line)

    def read(self, prompt):
        '''
        default read method. overwrite for other consoles
        '''
        line = raw_input(prompt)
        return line

    def write(self, output):
        '''
        default write method. overwrite for other consoles
        '''
        print output

    def stop(self):
        '''
        Stops console
        '''
        self.running = False

    def print_help(self):
        '''
        Prints help
        '''

        self.write("Available commands. Type 'help <command>' for specific help.")
        self.write("")
        
        for key, _ in self.helpers.items():
            #self.write("** %s '%s'-> %s" %(key, value['sintax'], value['help']))
            self.write( "** %s" % key)


class TelnetConsoleProvider(utils.ZThread):

    '''
    Provides new telnet consoles
    '''

    core = None
    listener = None
    connections = {}
    consoles = []
    port = None
    running = False
    klass = None
    
    def __init__(self, *args, **kw):
        
        utils.ZThread.__init__(self, *args, **kw)
        
        self.core = kw['core']
        self.klass = kw.get('klass')
        self.name = kw.get('name', '**')        
                
    def run(self):

        '''
        Console start
        '''

        self.port = self.core.configManager.get_int('Console', 'port')
        
        if not self.port:
            log.error("Console could not be started !!")
            return
        
        self.running = True
        
        self.listener = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.listener.bind(('0.0.0.0', self.port))
            self.listener.listen(1)
            #self.is_ok = True
            log.info("TelnetConsole is at localhost:%d" % self.port )
        except Exception, why:
            log.error('Telnet console could not be binded to port %d [%s]' % (self.port, why) )
        
        while self.running:
            #log.info("TenletConsole running")
            utils.ZThread.run(self)
            try:
                _rx, _, _ = select.select([self.listener], [], [], 1.0)
                if _rx:
                    new_client = self.listener.accept()
                    console = self.klass(parent=self, socket=new_client, name=self.name, core=self.core)
                    self.connections[new_client[0]] = (new_client[1], time.time())
                    self.consoles.append(console)
                    console.hello()
                    console.start()
            except Exception, why:
                dummy = 1

        log.info("TelnetConsole stopped")
                
    def purge_connection(self, _socket):
        '''
        Removes connection
        '''
        self.connections.pop(_socket)
        
    def stop(self):
        '''
        stop specific tasks
        '''
        self.running = False
        try:
            self.listener.close()
        except Exception, why:
            log.warning("listener close fail: %s" % why)
        for cons in self.consoles:
            cons.stop()
        
            
class TelnetConsole(Console):
    '''
    Telnet console
    '''

    client_addr = None
    client = None 
    buffer = None
    port = None
    name = None
    logged_date = None
    core = None

    reg_who = re.compile(r"(?P<cmd>who)", re.DOTALL | re.MULTILINE)
    
    def __init__(self, *args, **kw):
        
        self.core = kw['core']
        self.parent = kw.get('parent')
        self.name = kw.get('name', '**')
        self.client = kw.get('socket')
        self.client_addr = self.client[1]
        self.client = self.client[0]
        self.logged_date = time.time()
        self.buffer = StringIO.StringIO()
        
        Console.__init__(self, *args, **kw )
        
        log.info("Starting telnet console from %s:%s" % (self.client_addr[0], self.client_addr[1]))
        
        helpers = {'who':{'reg':self.reg_who, 'func':self.helper_who, 'sintax':'who', 'help':'Show current connections'},}
        self.public_commands.extend(['who'])
        self.helpers.update(helpers)

    def helper_who(self, **kw):

        '''
        Shows corrent opened connections
        '''

        assert kw.get('cmd') == 'who'
        
        for conn in self.parent.connections.values():
            if conn[0] == self.client_addr:
                preffix = "(this)"
            else:
                preffix = ""
            fecha = utils.datetime_2string(conn[1])
            text = "%s from %s:%s %s" % (fecha, conn[0][0], conn[0][1], preffix)
            self.write(text)
            
    def stop(self):
        self.running = False
        if self.client is not None:
            self.write('')
            self.client.close()

    def hello(self):
        '''
        Wellcome message
        '''

        text = (
                    "Wellcome to %s console. cnn 2013" % self.name,
                    "---------------------------------------------",
                    "",
                    "TIP: write 'help' for help",
                    "TIP: in linux, if you use 'rlwrap telnet <host> <port>',",
                    "     you will have arrows history in your telnet session !!",
                    "",
                    "Enjoy !!"
               )

        # Just for beauty and avoid writting #####.....
        size = 0
        for line in text:
            size = max(size, len(line))

        self.write('*'*size)
        for line in text:
            self.write(line)
        self.write('*'*size)
        
        self.print_help()


    def close_client(self):
        log.info("Closed telnet console from %s:%s" % (self.client_addr[0], self.client_addr[1]))
        self.client.close()
        self.parent.purge_connection(self.client)
        self.client = None

    def read(self, prompt):

        # send pending responses
        if self.buffer.getvalue() and self.client:
            self.client.send(self.buffer.getvalue())
            self.buffer.truncate(0)


        if self.client:
            sockets = [self.client]
            self.client.send(prompt)
        else:
            sockets = []

        _rx, _, _ = select.select(sockets, [], [], 99999)
        if _rx:
            raw = self.client.recv(0xffff)
            if raw == '':
                self.client.close()
                self.client = None
            else:
                raw = raw[:-2]
            return raw
        
        return ''

    def write(self, output):

        try:
            self.client.send('%s\r\n' % output)
        except Exception, why:
            log.info("Could not write to console [%s]" % why)


