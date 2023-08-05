# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:35:58 2018

@author: ThomasBitskyJr
(C) Copyright 2018-2020 Autoamted Design Corp. All Rights Reserved.

Combines a Beckhoff ADS client with loosely-coupled events for
easy integration into a larger program.

"""

from .ads_client import AdsClient
from .events import Events


import pyads
import asyncio
import sys, traceback
import time
import os

import logging, logging.handlers
import configparser
from typing import Dict,Any


# Create a named logger instance
log = logging.getLogger(__name__)
    

class AdsManager():
    """Combines a Beckhoff ADS client with loosely-coupled events for
    easy integration into a larger program.
    """

    def __init__(self, domain:str, options : configparser.ConfigParser) -> None:
        """Constructor

        Parameters
        ----------

        domain : str
            The domain for this connection. Could also be termed the 
            "connection name." Used for routing signals to and from 
            a particular instance.

        options : ConfigParser
            Configuration options from an .ini file.
        """
        self.options:configparser.ConfigParser = options
        self.ads_client:AdsClient = None

        if domain == None or len(domain) == 0:
            raise Exception("Invalid argument: domain must not be a blank string.")

        self.domain = domain


    def configure_signals(self) -> None:
        """Create the slots for the loosely-coupled API and
        attach to the signals.
        """

        async def on_subscribe_tag(args) -> None:
            """Slot
            
            Request to register a tag for on-change notification.
            """
            if ( not type(args) is dict ):
                msg = "on_subscribe_tag argument must be a dictionary"
                log.error(msg)
                raise Exception(msg)
            else:       
                self.ads_client.add_tag(args)
                await self.ads_client.refresh(args["symbol"])


        async def on_refresh_all(args) -> None:
            """Slot
            
            Request to re-broadcast the current value for all registerd tags.
            """            
            await self.ads_client.refreshAll()

        async def on_refresh_tag(args : str):
            """Slot
            
            Request to re-broadcast the current value for a specific tag.
            """                 

            try:
                await self.ads_client.refresh(args)

            except:
                log.error(f"Failed to refresh requested tag. {args}")


        async def on_tag_write(args:dict) -> None:
            """Slot
            
            Request to re-broadcast the current value for all registerd tags.
            """                 
            if type(args) is dict:
                await self.ads_client.writeTag(args.get("name"), args.get("value"))
            else:
                log.warning("AdsManager::on_tag_write - invalid argument.")


        # async def on_data_change(args:dict) -> None:
        #     """Callback from Ads Client. Notification from the remote
        #     controller that the value of a tag has changed.            
        #     """            
        #     try:
        #         # publish the tag value under the tag name

        #         log.debug( f"ADS DATA CHANGE name: {args.get('name')} value: {args.get('value')}")

        #         Events.publish(args.get("name"), args.get("value"))
        #     except Exception:
        #         log.error( "Exception on publish {0}  {1}".format(args.get("name"), args.get("value")))

        # Events.subscribe_method(f"{self.domain}/ads-dataChange", on_data_change)


        Events.subscribe_method(f"{self.domain}/ads-subscribe-tag", on_subscribe_tag)
        Events.subscribe_method(f"{self.domain}/ads-refresh-all", on_refresh_all)
        Events.subscribe_method(f"{self.domain}/ads-refresh-tag", on_refresh_tag)
        Events.subscribe_method(f'{self.domain}/ads-tag-write', on_tag_write )


    def start(self) -> None:
        """Configure the ads manager and start a connection out to
        the configured PLC.
        """

        self.configure_signals()

        # Create an ads client instance, passing in the connection properties.

        options = {
            "amsnetid" : self.options["ADS"]['amsnetid'],
            "port" : self.options["ADS"].getint("port")
        }

        self.ads_client = AdsClient(options)

        try:
            # start the connection to the server

            log.info( "Connecting to ADS server.. ")
            log.info( "Note: If not connected to machine or local instance, this will block ")
            log.info( "and you will not be able to test.")

            self.ads_client.connect()
        except pyads.ADSError as ex:

            log.exception(ex)
            raise ex

        except Exception as ex:

            log.exception(ex)
            raise ex       


    def stop(self) -> None:
        """Disconnect the ADS client and unregister all tags.
        """
        if not self.ads_client is None:
            self.ads_client.unloadTags()
            self.ads_client.close()   


    async def start_async(self) -> None:
        """
        A callback that starts the server. Used when starting this class as a Windows Service or daemon.

        Usage:
        asyncio.run_coroutine_threadsafe(adsManagerInst.start_async(), loop)
        """

        self.start()            



    def add_tag(self, args : Dict[str,Any]) -> None:
        """Register a tag for communication with the remote ADS device.
        Typically, the tag will be registered for onchange notification.

        tag : dict
            {
                "symbol" : required. Full and complete name of variable symbol in remote device.
                "name" : required. Name that will be used to identify this locally within the client.
                "cycleTime" : Optional. Milliseconds. A minimum update rate.
                    Use this option when a remote symbol is changing too frequently.
                "subscription" : str. Optional. Specify if this is an "onchange" or "cyclic" type of
                    subscription, or specify "none" to no notification. 
                    Any other values will default to "onchange".
                    Default: "onchange"
            }
        """ 

        if not "symbol" in args:
            msg = "Invalid argument format: symbol required."
            log.error(msg)
            raise Exception(msg)

        if not "name" in args:
            msg = "Invalid argument format: name required."
            log.error(msg)
            raise Exception(msg)


        notify = True

        if "subscription" in args:
            subscription = args["subscription"].lower()

            if subscription == "none" or subscription == "cyclic":
                notify = False

        self.ads_client.add_tag(args, notify)

            










