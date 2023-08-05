# -*- coding: utf-8 -*-
"""
@author: Thomas Bitsky Jr
(C) Copyright 2020-2021 Automated Design Corp. All Rights Reserved.

A one-to-many pub/sub class for supporting global events
and loose coupling of APIs. Uses asyncio for non-blocking publication
of events.

Topics can be subscribed to either onchange (default) to save
bandwidth, or ALL so that the event is always received.

"""


"""
Important!
Disable ctrl-c causing an exception and blocking graceful shutdown.
"""
from typing import AnyStr, Callable
import time
import logging
import asyncio
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'


from .util import what_called_me

# Create a named logger instance
log = logging.getLogger(__name__)


class Events(object):
    """A simple one-to-many pub/sub class for supporting global events.
    Requires asyncio

    Usage
    -----

        Asynchronous:

        @Events.subscribe("hello")
        async def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)

        @Events.subscribe("hello")
        async def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)

        Events.publish("hello", "There")

        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}


        Blocking:
        @Events.subscribe("hello")
        def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)

        @Events.subscribe("hello")
        def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)

        Events.publish_sync("hello", "There")

        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}


    """

    subs = {}

    SUBSCRIBE_ALL_EVENTS = 0
    SUBSCRIBE_ONCHANGE = 1

    @staticmethod
    def add_subscribe(
        event: str,
        func,
        subscription_type: int = SUBSCRIBE_ONCHANGE,
        include_topic: bool = False
    ):
        """Subscribe the method of a class instance to an event id.
        Can't use a decororator for this because 'self' won't be created.

        Not required for static methods. In that case, use the subscribe decorator.

        Parameters
        ----------
        event : str
            ID of the event

        func : function
            The method/slot to call back.

        subscription_type : int
            Specify whether to receive a signal only when the value
            has changed (default) or every time the value is published.

        include_topic : bool
            Included the published topic as an argument. Requires that
            the target method accepts the topic string as the first parameter.
            i.e.  my_target_method(topic:str, value:Any)
        """

        should_publish = False
        value = None

        if event not in Events.subs:
            Events.subs[event] = []
        else:
            if subscription_type == Events.SUBSCRIBE_ONCHANGE:
                value = Events.subs[event][0]["last_value"]

                if value != None:
                    should_publish = True

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        ev = {
            "func": func,
            "loop": loop,
            "topic" : event,
            "subscription_type": subscription_type,
            "last_value": value,
            "include_topic" : include_topic
        }

        Events.subs[event].append(ev)

        if should_publish:
            Events._publish_event(ev, *value)

    @staticmethod
    def unsubscribe_method(event: str, func: Callable) -> None:
        """Remove the subscription on a topic for a particular
        function.
        """
        if event in Events.subs:

            newlist = []

            for item in Events.subs[event][:]:
                if "func" in item:
                    if item["func"] != func:
                        newlist.append(item)

            Events.subs[event] = newlist

    @staticmethod
    def subscribe_method(event: str,
                         func: Callable,
                         subscription_type: int = SUBSCRIBE_ONCHANGE,
                         include_topic: bool = False
                         ) -> None:
        """Subscribe the method of a class instance to an event id.
        Can't use a decororator for this because 'self' won't be created.

        Not required for static methods. In that case, use the subscribe decorator.

        Parameters
        ----------
        event: str
            ID of the event

        func: function
            The method/slot to call back.

        subscription_type: int
            Specify whether to receive a signal only when the value
            has changed(default) or every time the value is published.

        include_topic: bool
            Included the published topic as an argument. Requires that
            the target method accepts the topic string as the first parameter.
            i.e.  my_target_method(topic: str, value: Any)

        """
        Events.add_subscribe(
            event, 
            func, 
            subscription_type=subscription_type,
            include_topic=include_topic
        )

    @staticmethod
    def subscribe(event: str, subscription_type: int = SUBSCRIBE_ONCHANGE) -> None:
        """Subscribe a function  to an event ID.

        Parameters
        ----------
        event: str
            ID of the event

        """

        def wrap_function(func: Callable):

            Events.add_subscribe(event, func, subscription_type)
            return func
        return wrap_function

    @staticmethod
    def _publish_event(ev, *args, **kwargs):

        if asyncio.iscoroutinefunction(ev["func"]):

            loop = ev["loop"]  
            asyncio.run_coroutine_threadsafe(ev["func"](*args, **kwargs), loop)
            
        else:

            ev["func"](*args, **kwargs)


    @staticmethod
    def publish(event: str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID.

        For coroutine functions defined with async, returns immediately. The
            callback is scheduled into the event loop.
        Synchronous functions are executed in order and block untile done.
        """

        if event in Events.subs:

            try:

                for ev in Events.subs[event]:


                    should_publish = False
                    if ev["subscription_type"] == Events.SUBSCRIBE_ALL_EVENTS:
                        should_publish = True
                    elif ev["subscription_type"] == Events.SUBSCRIBE_ONCHANGE:
                        if args != ev["last_value"] or ev["last_value"] == None:
                            should_publish = True

                    if should_publish:

                        if not ev["include_topic"]:
                            Events._publish_event(ev, *args, **kwargs)
                        else:
                            # in this case, we include the topic name as the first argument
                            Events._publish_event(ev, event, *args)

                        ev["last_value"] = args

            except Exception as e:
                logging.warning(f"Exception processing event {event} :\n {e}")

    @staticmethod
    def publish_sync(event: str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID. SYNCHRNOUS AND BLOCKING.

        """
        try:
            for ev in Events.subs[event]:
                try:
                    ev["func"](*args, **kwargs)
                except Exception as e:
                    Events.logger(f"{e}")
        except:
            pass

