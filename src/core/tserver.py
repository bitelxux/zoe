#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZOE. A P2P messaging system

(c) Carlos Novo 2013
Universidad de Sevilla

*******************************************************************
TServer module
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


import traceback
import threading
import time

from utils import utils
log = utils.log

DEBUG = False
PAUSE = 1.0/1000

class TServer(utils.ZThread):

    '''
    The heart of the beast. A threaded server with three activities queues with
    High, Medium and Low priority.
    '''

    Q_HIGH = 'H'
    Q_MEDIUM = 'M'
    Q_LOW = 'L'

    h_counter = 0
    m_counter = 0
    l_counter = 0

    running = False
    lapse = None  
    pending_activities = []
    done_activities = {}
    activity_id = 0
    lock = threading.RLock()

    _current_queue = Q_HIGH
    activities = {'H':[], 'M':[], 'L':[]}
    timers = {}
    
    name = None

    def __init__(self, *args, **kw):

        self.name = None
        
        self.h_counter = 0
        self.m_counter = 0
        self.l_counter = 0

        self.running = False
        self.lapse = None  
        self.pending_activities = []
        self.done_activities = {}
        self.activity_id = 0

        self._current_queue = self.Q_HIGH
        self.activities = {'H':[], 'M':[], 'L':[]}    
        self.timers = {}

        self.t_wd = time.time()

        utils.ZThread.__init__(self, *args, **kw)

    def stop(self):
        '''
        Specific stop tasks
        '''
        self.remove_timers()
        self.running = False

    def remove_timers(self):
        '''
        Removes timer
        '''
        for timer, _ in self.timers.items():
            del(self.timers[timer])

    def attend_timers(self):
        '''
        Attends timers
        '''
        for _, activity in self.timers.items():
            if time.time() > activity['next']:
                self.rearm_timer(timer=activity)
                new_activity = dict(activity)
                self.activity(**new_activity)

    def do_pulse(self):
        '''
        This is tserver one loop
        '''

        try:

            time.sleep(PAUSE)

            #if self.name == 'modbus':
            #  print "modbus [%d][%d][%d]" %(len(self.activities['H']), len(self.activities['M']), len(self.activities['L']) )

            self.attend_timers()

            if time.time() - self.t_wd > 15:
                self.t_wd = time.time()
                utils.ZThread.run(self)

            #log.info("Running %s" % self.name)
            if self._has_pending_activities():

                self.lock.acquire()
                activity = self.pop_activity()
                self.lock.release()

                if not activity:
                    return

                cond = time.time() - activity['ts'] > activity['wait']
                if cond:
                    if activity['callback']:
                        activity['callback'](result='timeout')
                    else:
                        log.warning("timeout %s %s" % (self.name, activity['method']))
                        activity['result'] = 'timeout'
                        self.done_activities[activity['id']] = activity            
                    return
                else:
                    pass

                t = time.time()
                # Si la actividad tiene que esperar respuesta, se descuenta
                # lo que se ha tardado en lanzar la actividad
                wait = activity['wait'] - (time.time()-activity['ts'])
                result = activity['method'](wait=wait, **activity['kw'])
                lapse = time.time() -t

                if lapse > 2.0:
                    log.warning("TSERVER [%0.3f] %s.%s [%s] (%s)" %(lapse, activity['priority'], 
                                                                 activity['method'].im_class.__name__, 
                                                                 activity['method'].im_func.__name__, 
                                                                 activity['kw']))

                if activity['type'] == 'blocking':
                    #if time.time() - activity['ts'] > activity['wait']:
                    #  continue # ya no da tiempo
                    activity['result'] = result
                    self.done_activities[activity['id']] = activity
                elif activity['callback']:
                    activity['callback'](result=result, lapse=lapse)

        except Exception, why:
            log.error("OOOOPS tserver.run %s: %s" % (self.name, why) )
            log.error(traceback.format_exc())

    def run(self): 
        '''
        tserver main loop
        '''
        self.running = True

        while self.running is True:
            self.do_pulse()

        log.info("TServer %s stopped" % self.name)


    def rearm_timer(self, timer):
        '''
        Rearms timer for next execution
        '''

        timer['next'] = time.time() + timer['timer']

    def wait_activity(self, **kw):  
        '''
        Insert new blocking activity in tserver
        '''
        assert 'callback' not in kw

        kw.setdefault('wait', 5.0)

        try:

            kw['type'] = 'blocking'
            activity_id = self.activity(**kw)
            t = time.time()

            while self.running and time.time()-t < kw['wait']:
                if activity_id in self.done_activities.keys():
                    result = self.done_activities.pop(activity_id)['result']
                    return result, time.time()-t
                time.sleep(0.001)


            if self.done_activities.get(activity_id):
                self.done_activities.pop(activity_id) 

        except Exception, why:
            log.error('OOOPS tserver.wait_activity %s: %s' % (self.name, why) )

        return None, time.time()-t

    def new_id(self):
        '''
        Trivial id generator
        '''
        self.activity_id += 1
        return self.activity_id

    def prepare_activity(self, **kw):  
        '''
        Prepares activity for insertion
        '''

        if kw.get('activity_id'):
            kw.pop('activity_id')
        else:  
            self.activity_id += 1

        priority = kw.get('priority', 'M') 
        wait = kw.pop('wait')
        method = kw.pop('method')
        callback = kw.pop('callback', None)

        activity = {}

        activity['timer'] = kw.get('timer')
        if kw.get('timer'):
            activity['skeep'] = kw.get('skeep', 0)

        activity['priority'] = priority
        activity['type'] = kw.get('type')

        # clean kw
        if kw.get('timer'):
            kw.pop('timer')
        if kw.get('skeep'):
            kw.pop('skeep')    
        if kw.get('type'):
            kw.pop('type')
        if kw.get('priority'):
            kw.pop('priority')
        #

        # if is timer
        if activity.get('timer'):
            activity['next'] = time.time() + activity['skeep']*activity['timer'] 
        #

        activity['id'] = self.new_id()
        activity['wait'] = wait
        activity['method'] = method
        activity['callback'] = callback
        activity['kw'] = kw
        activity['ts'] = time.time()
        activity['result'] = None

        return activity

    def timer(self, **kw):
        '''
        Inserts new timer
        '''
        kw.setdefault('wait', 120)
        activity = self.prepare_activity(**kw)
        self.timers[kw['name']] = activity

    def activity(self, **kw):
        '''
        Adds not blocking activity
        '''
        
        kw.setdefault('wait', 30)
        
        try:
            activity = self.prepare_activity(**kw)

            self.lock.acquire()
            self.activities[activity['priority']].append(activity)
            self.lock.release()

        except Exception, why:
            log.error('OOOPS tserver.activity %s:%s' % (self.name, why) )

        return activity['id']


    def _has_pending_activities(self):
        '''
        Helper
        '''
        return ( self.activities['H'] or self.activities['M'] or self.activities['L'] )

    def pop_activity(self):

        '''
        Gestion de colas
        Las tres colas están organizadas de manera circular:
        H->M->L->H
        Solo cambiamos de cola si la cola actual esta vacia o si se ha alcanzado el tope
        de la ráfaga y ADEMAS alguna de las colas siguientes tiene datos.
        '''

        _queue = None

        try:

            _info = None

            if self._has_pending_activities() == False:
                return _info

            if self._current_queue == self.Q_HIGH:
                if len(self.activities['H']) == 0 or self.h_counter >= 99:
                    if len( self.activities['M'] ) > 0:
                        #log.info( "Switching to MEDIUM priority queue" )
                        self._current_queue = self.Q_MEDIUM
                    elif len( self.activities['L'] ) > 0:
                        #log.info( "Switching to LOW priority queue" )
                        self._current_queue = self.Q_LOW
                    self.h_counter = 0

            if self._current_queue == self.Q_MEDIUM:
                if len( self.activities['M'] ) == 0 or self.m_counter >= 9:
                    if len( self.activities['L'] ) > 0:
                        #log.info( "Switching to LOW priority queue" )
                        self._current_queue = self.Q_LOW
                    elif len( self.activities['H'] ) > 0:
                        #log.info( "Switching to HIGH priority queue" )
                        self._current_queue = self.Q_HIGH
                    self.m_counter = 0

            if self._current_queue == self.Q_LOW:
                if len( self.activities['L'] ) == 0 or self.l_counter >= 1:
                    if len( self.activities['H'] ) > 0:
                        #log.info( "Switching to HIGH priority queue" )
                        self._current_queue = self.Q_HIGH
                    elif len( self.activities['M'] ) > 0:
                        #log.info( "Switching to MEDIUM priority queue" )
                        self._current_queue = self.Q_MEDIUM
                    self.l_counter = 0

            _queue = self._current_queue

            if not _queue:
                log.warning( "MMmmmmm _queue es None. Nunca debería pasar !!" )
                return _info

            if _queue == self.Q_HIGH:
                _info = self.activities['H'].pop(0)
                self.h_counter += 1
            elif _queue == self.Q_MEDIUM:
                _info = self.activities['M'].pop(0)
                self.m_counter += 1
            elif _queue == self.Q_LOW:
                _info = self.activities['L'].pop(0)
                self.l_counter += 1
            else:
                log.error( 'Oops incorrect queue: %s' %(_queue) )
        except Exception, why:
            log.error('OOOOPS tserver.popactivity %s:%s' % (self.name, why))
        finally:
            pass

        return _info

if __name__ == "__main__":

    dummy = 1





