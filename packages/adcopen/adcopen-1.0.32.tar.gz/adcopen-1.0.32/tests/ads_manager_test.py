
import pyads
import asyncio
import sys, traceback
import time
import os

import logging, logging.handlers
import configparser

from adcopen.ads_manager import AdsManager
from adcopen.events import Events


# Create a named logger instance
log = logging.getLogger(__name__)


if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    Set server configuration in adsmantest.ini file.
    """

    @Events.subscribe("PLC/GM.nHeartbeatCount")
    def on_heartbeat_changed(value):
        print(f"Heartbeat is now {value}")

    CONFIG_FILE_NAME:str = "adsmantest.ini"
    config = configparser.ConfigParser()
    if os.path.isfile(CONFIG_FILE_NAME):
        config.read(CONFIG_FILE_NAME)
    else:
        config['ADS'] = {
            "amsnetid": "", 
            "port": 851
        }

        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:

        manager:AdsManager = AdsManager("PLC", config)
        manager.start()

        manager.add_tag({"symbol":"GM.nHeartbeatCount", "name": "PLC/GM.nHeartbeatCount"})
        
        
        print( "Press CTRL-C to stop.")  

        loop.run_forever()

    except KeyboardInterrupt:
        
        print( "Closing from keyboard request.")  


    except Exception as ex:

        log.exception( f"AdsManager exception: {ex}")  
        #print(traceback.format_exc())

            
    finally:
        

        manager.stop()       
        
        loop.stop()

        print( "Goodbye.")
