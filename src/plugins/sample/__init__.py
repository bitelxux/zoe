# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
Zoe plugin sample
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

import sample

instance = None

# pylint: disable-msg = W0603

def run(core):
    '''
    Instances plugin and starts it
    '''
    global instance
    instance = sample.Sample(name='sample', core=core)
    # pylint: disable-msg = E1101
    instance.start()
  
