'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Friday, 12th March 2021 12:23:59 pm
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''

from time import sleep
from typing import Any
from timeit import default_timer as timer
from datetime import timedelta
from adcopen import Events
import logging
import asyncio


class Ton:
    """Timer On Delay class, analogous to an industrial PLC timer. 
    Starts counting to PRESET once IN is true, and only so long as In is true.

    Attributes
    ----------
    preset_ms : int
        Preset value of the timer, in milliseonds.
    userdata : Any
        Optional data that can be attached to the instance. Ignored by Ton.
    monitor_topic : str
        Optional. An event topic to monitor. When true, the Ton will count,
        when false, the Ton will reset.
    signal : str
        Optional. When output state of the Ton goes true, the ton will publish
        an event with this signal name.        
    signalled : bool
            State of the Ton when last checked. 
    """

    preset_ms : int = 0
    userdata : Any = None
    _monitor_topic : str = None
    signal  : str = None

    _start_time : float = None
    _signaled : bool = False
    _preset_sec : float
    _in : bool = False

    def __init__(
        self,
        preset_ms:int = None, 
        userdata:Any=None, 
        monitor_topic:str=None,
        signal:str=None
    ) -> None:

        if not preset_ms == None:
            self.preset_ms = preset_ms
        else:
            self.preset_ms = 0

        self._preset_sec = self.preset_ms / 1000

        self.userdata = userdata
        self.signal = signal
        self._signaled = False

        self.set_monitor_topic(monitor_topic)

    
    def set_preset(self, ms:int) -> None:
        """Set the preset time for the TON. Milliseconds.
        """
        self.preset_ms = ms
        self._preset_sec = self.preset_ms / 1000

    def set_userdata(self, s : Any) -> None:
        """Set the user data for the Ton.
        """
        self.userdata = s

    def set_monitor_topic(self, signal:str) -> None:
        """Sets a signal to monitor that will cause the Ton to start counting.
        When the signal is false, the Ton will reset.
        """

        if not signal == None:

            # Register monitoring this topic

            self._monitor_topic = signal


            def monitor_topic_changed(val):
                self.update(val)

            Events.subscribe_method(self._monitor_topic, monitor_topic_changed)
        
        
        elif not self._monitor_topic == None:

            # Unregister monitoring this topic
            # @todo: add this ability to the events library
            # supplying a second argument to the pop method ensures that
            # an exception will not be thrown if the topic has not be registered
            Events.subs.pop(self._monitor_topic, "") 

        else:
            self._monitor_topic = None



    def set_signal(self, signal:str) -> None:
        """Set a signal to broadcast on when the timer transitions from False to True.
        """
        self.signal = signal


    def reset(self) -> None:
        """Reset the state of the timer
        """        
        self._in = False
        self._start_time = timer()
        self._signaled = False
        self._preset_sec = self.preset_ms / 1000


    def start(self) -> None:
        """Start/reset the Ton counting programatically. Input is forced to true.
        Intended for use in state machines for which the Input/update() API is
        superfluous and the class is just being used for convenient calculation
        of time differentials.

        input is set to true, start_time is reset and the signaled state is
        reset to False. Note that if the update is called or input attribute 
        changed after calling this function, the values will be overridden.
        """ 
        self.reset()
        self._in = True


    def update(self, condition:bool) -> None:
        """Starts counting on rising edge of condition. Only counts so long
        as condition is true.
        """

        if not self._in and condition:
            self.start()
        elif self._in and condition and not self._signaled:
            self.q()

        self._in = condition

    def q(self) -> bool:
        """Returns true if the preset time has passed.
        """
        
        if self.preset_ms == None or self.preset_ms <= 0:
            return False

        if self._start_time == None:
            return False
        
        now = timer()

        # get seconds
        seconds = now - self._start_time
        if ( seconds >= self._preset_sec):

            if not self._signaled:

                if not self.signal == None and len(self.signal) > 0:
                    Events.publish(self.signal, self.userdata)

                self._signaled = True

            return True

        else:

            return False


    def elapsed_seconds(self) -> float:
        """Return the number of seconds that have elapsed since
        the timer was last started.
        """
        if self.preset_ms == None or self.preset_ms <= 0:
            return 0

        if self._start_time == None:
            return 0
        
        now = timer()

        # get seconds
        seconds = now - self._start_time
        return seconds


    def elapsed_string(self) -> str:
        """Return a formatted string of the elapsed time.
        """

        rc = self.elapsed_seconds()
        return timedelta(seconds=rc)
