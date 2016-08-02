#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Core module
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
import os
import imp

#sys.path.append('utils')
#sys.path.append('core')

from utils import utils
from console import console
from console import zoe_console
from storage import sqlite_db
from node import node
from net import net
from contacts import contacts

import publisher

log = utils.log


class Core(utils.ZThread):

    '''
   Core class. There should be only one.
   Singleton aproach was deprecated
   '''

    # App will be a nice Singleton
    #__metaclass__ = utils.Singleton

    plugins = {}
    started_at = time.time()
    running = False
    ready = False
    console = None
    configManager = None
    storage = None
    node = None
    net = None
    publisher = None
    contacts = None

    my_id = None
    app_path = None

    BUILD = '437'

    def __init__(self, *args, **kw):

        config_file = kw.get('config')
        
        self.app_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        
        if not config_file:
            log.info("Using default config.cfg")
            config_file = '%s/%s' % (self.app_path, 'config.cfg')
        else:
            log.info("Using %s config file" % config_file)

        
        self.configManager = utils.ConfigManager(name='config', config_file=config_file)
        self.my_id = self.configManager.get('General', 'id')
        
        self.publisher = publisher.Publisher(name='publisher')

        #self.load_plugins_from_config()
        utils.ZThread.__init__(self, *args, **kw)

    def load_plugins_from_config(self):
        '''
        loads plugins specified in config file
        '''

        # let some time to things go up
        time.sleep(0.1)
        
        plugins_path = os.path.join(self.app_path, 'plugins')
        plugins_list = self.configManager.get_list('General', 'plugins')

        if not plugins_list:
            log.info("Not plugins enabled")
            return

        for plugin in plugins_list:
            try:
                m = imp.load_module(plugin, *imp.find_module(plugin, [plugins_path]))
                m.run(core=self)
                self.plugins[plugin] = m.instance                
                log.info("Loaded plugin %s" % plugin)
            except Exception, why:
                log.error("Error loading plugin %s: %s" % (plugin, why))


    def load_plugins_from_dir(self):

        '''
        alternative for loading plugins instead from config, from existing at
        directory, the way apache does
        '''

        plugins_path = os.path.join(self.app_path, 'plugins')
        for _, dirnames, _ in os.walk(plugins_path):
            for plugin in dirnames:
                m = imp.load_module(plugin, *imp.find_module(plugin, [plugins_path]))
                m.run(core=self)
                self.plugins[plugin] = m.instance
                log.info("Loaded plugin %s" % plugin)

    def check_sanity(self):

        '''
        Checks needed modules are running otherwise launches them
        '''

        ##########################
        # Start storage
        ##########################
        if self.running and not self.storage:
            self.storage = sqlite_db.SqliteDB(name='storage', core=self)
            self.storage.start()

        ##########################
        # Start net
        ##########################
        if self.running and not self.net:
            self.net = net.Net(name='net', core=self)
            self.net.start()

        ##########################
        # Start node
        ##########################
        if self.running and not self.node:
            self.node = node.Node(name='node', core=self)
            self.node.start()

        ##########################
        # Start contacts support
        ##########################
        if self.running and not self.contacts:
            self.contacts = contacts.Contacts(name='contacts', core=self)
            self.contacts.start()
            
            
        ##########################
        # Start console
        ##########################
        if self.running and not self.console:
            self.console = console.TelnetConsoleProvider(klass=zoe_console.zoe_console, core=self, name='zoe')
            self.console.start()

    def run(self):

        '''
        Core loop
        '''

        self.running = True
        self.check_sanity()
        self.load_plugins_from_config()
        
        utils.RSA(config=self.configManager).check_rsa_keys()
        self.ready = True
 
        while self.running:
            time.sleep(1.0)
            utils.ZThread.run(self)
            self.check_sanity()
            

    def stop(self):

        '''
        Stops all running modules and core
        '''

        self.running = False

        if self.console:
            self.console.stop()
        if self.storage:
            self.storage.stop()
        if self.node:
            self.node.stop()
        if self.net:
            self.net.stop()
        if self.publisher:
            self.publisher.stop()
        if self.contacts:
            self.contacts.stop()

        for plugin in self.plugins.values():
            plugin.stop()

        #time.sleep(1)










