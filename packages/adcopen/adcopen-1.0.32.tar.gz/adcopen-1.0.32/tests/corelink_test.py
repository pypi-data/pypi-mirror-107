'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Friday, 30th April 2021 8:46:10 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''

import logging
import asyncio

from adcopen.corelink import CoreLink, CoreLinkSignals, CoreLinkSlots, CoreLinkStopCodes
from adcopen.events import Events



# Create a named logger instance
log = logging.getLogger(__name__)
    


if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")

    @Events.subscribe(CoreLinkSlots.CONNECTED)
    async def connected(data):
        print("SLOT connected")

        asyncio.run_coroutine_threadsafe(test_datastore(), loop)


        await CoreLink.publish("test/dummy", "this is a test")


    @Events.subscribe("simulator/rand10")
    async def subscribe_test(data):
        print(f"Received simulator/rand10 value: {data}")

    
    @Events.subscribe("test/dummy")
    def dummy_test(data):
        print(f"\n\n ** DUMMMY TEST  {data} ** \n\n")


    async def test_datastore():

        print( "Let's test the datastore!")

        try:
            await CoreLink.create_datastore("corelink-test")
            await asyncio.sleep(delay=2)
            await CoreLink.create_datastore("corelink-test")
            await asyncio.sleep(delay=2)
            await CoreLink.set_datastore_value("corelink-test", "too many secrets")
            await asyncio.sleep(delay=2)
            rc = await CoreLink.get_datastore_value("corelink-test")

            print(f"Data store value: {rc}")

            await asyncio.sleep(delay=2)
            rc = await CoreLink.append_datastore_value("corelink-test", "setec astronomy")
            await asyncio.sleep(delay=2)
            rc = await CoreLink.get_datastore_value("corelink-test")

            print(f"Data store value: {rc}")

            print( "DataStore test complete.")

        except Exception as ex:
            log.exception(ex)


    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:

        print("First, test synchronous connection")
        CoreLink.connect("127.0.0.1", 8081)

        print(f"Am I connected? {CoreLink.is_connected}")


        print("Stop connection synchrnously...")
        CoreLink.disconnect()

        print("Restart with async method...")

        CoreLink.start("127.0.0.1", 8081)
        print( "Press CTRL-C to stop.")  



        loop.run_forever()

    except KeyboardInterrupt:
        
        print( "Closing from keyboard request.")  


    except Exception as ex:

        print( f"CoreLink exception: {ex}")  
        print(ex)
            
    finally:
        
        CoreLink.stop()       
        
        loop.stop()

        print( "Goodbye.")
