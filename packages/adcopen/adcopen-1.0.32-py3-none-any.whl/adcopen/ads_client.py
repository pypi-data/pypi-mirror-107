# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:49:50 2018

@author: ThomasBitskyJr


Uses pyads:
https://pyads.readthedocs.io/en/latest/quickstart.html#usage


Usage:
    
    from ads import AdsClient
    
    tags_ = [{'symbol': "GM.trayHomeOffsetWidth", "type": pyads.PLCTYPE_REAL},
         {'symbol': "GM.manualPressureCommand", "type": pyads.PLCTYPE_INT},
         {'symbol': "GM.isControlPower", "type": pyads.PLCTYPE_BOOL},
         {'symbol': "GM.intSim", "type": pyads.PLCTYPE_INT},
         {'symbol': "GM.floatSim", "type": pyads.PLCTYPE_REAL},
         {'symbol': "GM.dblSim", "type": pyads.PLCTYPE_LREAL}]
    
    
    
"""

import typing
import logging
import numpy as np
from struct import Struct
from ctypes import pointer, c_ubyte, c_ulong, c_ushort, sizeof, c_char_p, Structure, \
    c_bool, c_byte, c_int8, c_uint8, c_int16, c_uint16, \
    c_int32, c_uint32, c_float, c_double, c_char, c_short, c_int64, c_uint64, \
    c_int64
from ctypes import memmove, addressof
import pyads.filetimes
import pyads
import time
from typing import Dict, Any, List

from .events import Events

# Create a named logger instance
log = logging.getLogger(__name__)



class SAdsSymbolEntry(Structure):

    """
    ADS symbol information
    :ivar entryLength: length of complete symbol entry
    :ivar iGroup: indexGroup of symbol: input, output etc.
    :ivar iOffs: indexOffset of symbol
    :ivar size: size of symbol (in bytes, 0=bit)
    :ivar dataType: adsDataType of symbol
    :ivar flags: symbol flags
    :ivar nameLength: length of symbol name
    :ivar typeLength: length of type name
    :ivar commentLength: length of comment
    """
    _pack_ = 1
    _fields_ = [("entryLength", c_ulong),
                ("iGroup", c_ulong),
                ("iOffs", c_ulong),
                ("size", c_ulong),
                ("dataType", c_ulong),
                ("flags", c_ulong),
                ("nameLength", c_ushort),
                ("typeLength", c_ushort),
                ("commentLength", c_ushort)]


'''
' ADS Constants for data types.
'''
ADST_VOID = 0
ADST_INT8 = 16
ADST_UINT8 = 17
ADST_INT16 = 2
ADST_UINT16 = 18
ADST_INT32 = 3
ADST_UINT32 = 19
ADST_INT64 = 20
ADST_UINT64 = 21
ADST_REAL32 = 4
ADST_REAL64 = 5
ADST_BIGTYPE = 65
ADST_STRING = 30
ADST_WSTRING = 31
ADST_REAL80 = 32
ADST_BIT = 33


ADST_TYPE_TO_PLC_TYPE: dict = {
    ADST_VOID: None,
    ADST_BIT: pyads.PLCTYPE_BOOL,
    ADST_INT8: pyads.PLCTYPE_SINT,
    ADST_UINT8: pyads.PLCTYPE_USINT,
    ADST_INT16: pyads.PLCTYPE_INT,
    ADST_UINT16: pyads.PLCTYPE_UINT,
    ADST_INT32: pyads.PLCTYPE_DINT,
    ADST_UINT32: pyads.PLCTYPE_UDINT,
    ADST_UINT64: pyads.PLCTYPE_ULINT,
    ADST_INT64: c_int64,
    ADST_REAL32: pyads.PLCTYPE_REAL,
    ADST_REAL64: pyads.PLCTYPE_LREAL,
    ADST_STRING: pyads.PLCTYPE_STRING,
    ADST_WSTRING: pyads.PLCTYPE_STRING,
    ADST_REAL80: pyads.PLCTYPE_LREAL,
    ADST_BIGTYPE: None
}


class AdsClient():

    # constructor
    def __init__(self, options: Dict[str,any] = {}) -> None:
        """Constructor
        options : Dict[str,Any]
            Optional Communications settings.
            {
                "amsnetid" : 6-byte ADS address. Blank string defaults to local instance. 
                    Default: ""
                "port" : TwinCAT ADS task port. 
                    Default: 851
            }
        """

        amsNetId = "127.0.0.1.1.1"

        if "amsnetid" in options:
            # connect to TwinCAT on a remote machine
            amsNetId = options.get("amsnetid")

        if len(amsNetId) <= 0:
            # pyads doesn't handle empty strings properly
            amsNetId = "127.0.0.1.1.1"

        if "port" in options:
            port = options["port"]
        else:
            # The default PLC port
            port = 851

        self.handles_ = {}
        self.handlesByName_ = {}


        log.info(f"Configuring ADS client for net id: {amsNetId}  port: {port}")

        self.plc_ = pyads.Connection(amsNetId, port)


    def handleDataReceived(self, name: str, value: typing.Any, timestamp: typing.Any) -> None:
        """Handles publishing data when a value is received from the PLC.
        """
        args = {'name': name, "value": value, "timestamp": timestamp}
        Events.publish("ads-dataChange", args)
        Events.publish(name, value)

    def datachange_callback(self, notification, data):
        """A generic callback to receive datachange notitications from pyads.
        If a tag is configured to notify on data change, this method will be
        signaled by the ADS router with the updated information.

        Note that this function is called back from a C thread in the ADS router.

        Instead of having a decorator for every data type, this function uses 
        the handle data_type information we already stored to enable use of 
        the pyads parse_notification method.
        """

        tag : Dict[str,Any] = self.handlesByName_[data]

        handle, timestamp, value = self.plc_.parse_notification(
            notification, tag["type"])

        self.handleDataReceived(tag["tag_name"], value, timestamp)

    def add_tag(self, tag, notify=True):
        """Register a tag for communication with the remote ADS device.
        Typically, the tag will be registered for onchange notification.

        tag : dict
            {
                "symbol" : required. Full and complete name of variable symbol in remote device.
                "name" : required. Name that will be used to identify this locally within the client.
                "cycleTime" : Optional. Milliseconds. A minimum update rate.
                    Use this option when a remote symbol is changing too frequently.
            }

        notify : bool
            Register this tag for onchange notification.            
            Default: True.
        """

        if not isinstance(tag, dict):
            raise Exception("Tag argument must be a dict.")

        if not 'symbol' in tag:
            raise Exception("'symbol' must be specified in tag argument.")


        if not 'name' in tag:
            raise Exception("'name' must be specified in tag argument.")


        '''
        ' Don't re-register if this tag was already requested.
        ' Not an error, so just return gracefully.
        '''
        if tag.get('symbol') in self.handlesByName_.keys():
            log.info(
                "Symbol {0} already registered. Ya' basic.". format(tag.get('symbol')))
            return

        # cycle time should be a real number that comes in milliseconds

        if 'cycleTime' in tag.keys():

            cycleTime = tag.get('cycleTime')
            # print( "cycleTIme {0} tag {1}".format(cycleTime, tag.get('symbol')))

        else:
            # our interface shouldn't need anything over 100ms
            # If a tag needs more update, send in a cycleTime of 0
            cycleTime = 100

        try:
            symbol = tag.get('symbol')
            tagInfo = self.readSymbol(symbol)
        except Exception as ex:
            log.error(
                f"Exception validating symbol name {symbol} in remote device: {ex}"
            )
            return

        '''
        ADST_INT8     = 16
        ADST_UINT8    = 17
        ADST_INT16    = 2
        ADST_UINT16   = 18
        ADST_INT32    = 3
        ADST_UINT32   = 19
        ADST_INT64    = 20
        ADST_UINT64   = 21
        ADST_REAL32   = 4
        ADST_REAL64   = 5
        ADST_BIGTYPE  = 65
        ADST_STRING   = 30
        ADST_WSTRING  = 31
        ADST_REAL80   = 32
        ADST_BIT      = 33
        '''

        handle = -1
        user = -1
        tagType = None

        log.info("adding notification: {0} {1}".format(
            tag.get('symbol'), tagInfo.dataType))

        if tagInfo.dataType in ADST_TYPE_TO_PLC_TYPE:
            tagType = ADST_TYPE_TO_PLC_TYPE[tagInfo.dataType]
        else:
            raise Exception("This type is unsupported.")

        if notify:
            """API changes in pyads:
            - cycle_time and max_delay are now in milliseconds
            - arguments of datachange_callback have changed.
            """

            handle, user = self.plc_.add_device_notification(
                tag.get('symbol'),
                pyads.NotificationAttrib(
                    sizeof(tagType), cycle_time=cycleTime, max_delay=cycleTime),
                self.datachange_callback
            )

            log.info(f"added notify: {handle} {user} {sizeof(tagType)}")

        self.handles_[handle] = ({"handle": handle, 
                                "user": user, 
                                'symbol': tag.get('symbol'),
                                "value": 0, 
                                "type": tagType,
                                "tag_name" : tag.get('name')
                                }
                                )
        self.handlesByName_[tag.get('symbol')] = self.handles_[handle]


    def loadTags(self, tags : List[Dict[str,Any]]):
        """Load tags from a array of dictionaries.

        Parameters
        ----------
        tags : List[Dict[str,Any]]
            An array of the tags to be added.
        """

        log.info("Adding tags from dictionay...")

        shouldExit = False

        while not shouldExit:
            try:
                for i in range(len(tags)):

                    self.add_tag(tags[i])
                    shouldExit = True

            except pyads.pyads_ex.ADSError:
                log.warning("Communication error. Retrying...")
                time.sleep(2)
            except:
                raise Exception("Critical communications error.")


    def unloadTags(self):
        """Delete the notification for registered onchange tags in
        the ADS router. Otherwise, the ADS router gets bogged down
        and becomes unusable.
        """

        log.info("Removing tags...")

        for key, value in self.handles_.items():

            if (value.get("handle") > 0):
                log.info("removing handle {0} {1}"
                             .format(value.get("handle"), value.get("user"))
                             )
                self.plc_.del_device_notification(
                    value.get("handle"), value.get("user"))

        log.info("Handles are removed...")


    async def refreshAll(self):
        """Refresh any stale values for registered notification tags by
        doing a synchrnous read of the tag in the plc.
        """

        for key, value in self.handlesByName_.items():

            try:
                log.info("refresh {0} {1}".format(key, value.get("type")))
                value = self.plc_.read_by_name(key, value.get("type"))
            except:
                value = 0

            args = {'symbol': key, "value": value}
            await Events.publish("ads-dataChange", args)

    async def refresh(self, tagName):

        if tagName in self.handlesByName_.keys():
            tag = self.handlesByName_[tagName]

            try:
                value = self.plc_.read_by_name(tagName, tag["type"])

                args = {'symbol': tagName, "value": value}
                await Events.publish("ads-dataChange", args)

            except:
                log.error("Failure to refresh tag {0}".format(tagName))

    # start a connection to the remote server

    def connect(self):
        self.plc_.open()

    def close(self):
        self.plc_.close()

    def readSymbol(self, name):

        err_code = 0

        try:

            address = self.plc_._adr

            '''
            ' Updated 2018 08 22
            ' Newer version of pyads changed the api to use AdsSyncReadWriteReqEx2 instead
            ' of AdsSyncReadWriteReq, and also changed the name of the file, so pyads.pyads becomes
            ' pyads.pyads_ex
            '''
            adsSyncReadWriteReqFct = pyads.pyads_ex._adsDLL.AdsSyncReadWriteReqEx2

            ADSIGRP_SYM_INFOBYNAMEEX = 0xF009
            rdata = SAdsSymbolEntry()

            pAmsAddr = pointer(address.amsAddrStruct())
            nIndexGroup = c_ulong(ADSIGRP_SYM_INFOBYNAMEEX)
            nIndexOffset = c_ulong(0)

            nReadLength = c_ulong(sizeof(rdata))

            # We got the name as unicode string (python 3)
            # we have to convert it to ascii
            ascii_string = name.encode()
            data = c_char_p(ascii_string)
            data_length = len(name) + 1

            '''
            ' Updated 2018 08 22
            ' Newer version of pyads changed the api to use AdsSyncReadWriteReqEx2 instead
            ' of AdsSyncReadWriteReq, so we have to send the port number return by adsOpenPortEx
            ' as the first argument.
            '''
            port = self.plc_._port

            '''
            ' Updated 2018 08 22
            ' Newer version of pyads changed the api to use AdsSyncReadWriteReqEx2 instead
            ' of AdsSyncReadWriteReq. It returns the number of bytes returned in a pointer
            ' as the last argument.
            '''
            pcbReturn = c_ulong(0)

            err_code = adsSyncReadWriteReqFct(
                port,
                pAmsAddr,
                nIndexGroup,
                nIndexOffset,
                nReadLength,
                pointer(rdata),
                data_length,
                data,
                pointer(pcbReturn)
            )

        except:
            log.exception("reading symbol information")

        if err_code:
            ex = pyads.ADSError(err_code)
            log.exception(ex)
            raise Exception(ex)
        else:
            return rdata

    async def writeTag(self, tagName, value):

        if not tagName in self.handlesByName_.keys():

            try:
                # Fetch the tag properties, but don't register for notify.
                tagArg = {'symbol': tagName}
                self.add_tag(tagArg, False)
            except:
                log.error(
                    "Failed to write tag {0} b/c I couldn't get it's information.".format(tagName))

        if not tagName in self.handlesByName_.keys():
            log.error("Tag {0} was not found in PLC.".format(tagName))
            return

        tag = self.handlesByName_[tagName]

        try:
            self.plc_.write_by_name(tagName, value, tag.get("type"))
        except:
            log.error(f"Failed to write tag {tagName} {value}")

    '''
    ' Flatten the array
    ' The matrix columns must match the order of the
    ' 2D array columns in TwinCAT
    '''
    async def write2dArray(self, tagName, matrix):

        matRows = matrix.shape[0]
        matCols = matrix.shape[1]

        nLimit = matRows * matCols

        rc = np.zeros(nLimit)

        index = 0
        for i in range(matRows):
            for j in range(matCols):
                rc[index] = matrix.item(i, j)
                index += 1

        # @TODO: the library picks out the data type
        self.plc_.write_by_name(tagName, rc, pyads.PLCTYPE_ARR_LREAL(nLimit))

