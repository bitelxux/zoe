#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013

*******************************************************************
ZOE launcher
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

import sys
import os

import time
import argparse
from utils import utils

log = utils.log

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(basepath)

from core import core

if __name__ == "__main__":
   
    log.info("Starting Zoe")
    t = time.time()
    
    parser = argparse.ArgumentParser( description="zoe")
    parser.add_argument( '--config', dest='config_file', help='Config file (defaults to config.cfg)' )
  
    args = parser.parse_args()
    
    app = core.Core(name='core', config=args.config_file)
    # pylint: disable-msg = E1101
    app.start()
    
    while not app.running:
        time.sleep(0.01)
    
    while app.running:

        # nothing to do
        time.sleep(5.0)
        
       
    #app.stop()
       
    log.info("Zoe closing. Good Bye")

   
    
    
    
