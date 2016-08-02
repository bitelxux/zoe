#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Publisher module
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

log = utils.log

class Publisher():
    '''
    Publisher class
    '''
    
    subscriptors = {}
    name = None
    
    def __init__(self, **kw):
        self.name = kw['name']
        self.subscriptors = {}
        
    def subscribe(self, who, pattern, callback):
        '''
        Subscribe point
        '''

        # little help
        if pattern == '*':
            pattern = '.*'
            
        self.subscriptors.setdefault(who, {})
        self.subscriptors[who][pattern] = callback
        
    def publish(self, **kw):
        '''
        Publish event to subscribers
        '''
        what = kw['what']
        for _, subscription in self.subscriptors.items():
            for pattern, callback in subscription.items():
                if re.match(pattern, what, re.IGNORECASE):
                    t = time.time()
                    callback(**kw)
                    # dont let callback take more than 5 milliseconds
                    assert time.time() -t < 0.05
                    
    def stop(self):
        '''
        Does specific stop tasks
        '''
        dummy = 1
            
            
if __name__ == "__main__":
    
    pass
    
        
    
