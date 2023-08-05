'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Friday, 30th April 2021 8:41:51 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''

from adcopen.ads_client import AdsClient
import pyads.filetimes
import pyads
import time

'''
A script for testing this individual file. Only runs of the program is
started from this script.
'''
if __name__ == '__main__':

    def main_loop():
        while 1:
            # do your stuff...
            # print (plc.read_by_name("GM.trayHomeOffsetWidth", pyads.PLCTYPE_REAL))
            time.sleep(0.5)

    tags_ = [
        {'symbol': "GM.nHeartbeatCount", "name":"PLC/GM.nHeartbeatCount", "type": pyads.PLCTYPE_UDINT}
    ]

    try:

        # options = {"AmsNetId": "127.0.0.1.1.1", "port": 851}
        # options = {}
        options = {"amsnetid": "5.78.94.236.1.1", "port": 851}

        client = AdsClient(options)
        client.connect()


        client.loadTags(tags_)


        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        client.unloadTags()

        print('\nClosing the PLC....\n')
        client.close()
