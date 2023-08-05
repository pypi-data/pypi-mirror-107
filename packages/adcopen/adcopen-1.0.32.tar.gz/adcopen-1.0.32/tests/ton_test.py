'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Friday, 30th April 2021 8:51:40 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''

import asyncio
import logging

from adcopen.events import Events
from adcopen.ton import Ton


if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")


    @Events.subscribe("myton.DN")
    async def tondone(value):
        print(f"The TON is Done!  {value}")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


    async def test_basic():
        """Basic test using the Ton in a non-blocking scenario.
        Tests the use case of how a Ton is used in Structured Text.
        """

        print( "\n\n\nTest basic usage...")


        ton = Ton(signal="myton.DN")

        ton.set_preset(1000)
        ton.set_userdata("Basic Usage")
        ton.start()        

        while not ton.q():

            print(ton.elapsed_string())
            await asyncio.sleep(delay=0.1)

        print("Basic usage: TON is DONE")


    async def test_monitor():
        """In this test, the Ton isn't started from code, but by
        using asynchronous events.
        """


        print( "\n\n\nTest monitor_topic...")

        ton = Ton(signal="myton.DN")

        ton.set_preset(1000)
        ton.set_userdata("test_monitor usage")

        ton.set_monitor_topic("mysignal")

        await asyncio.sleep(delay=1)
        
        print("monitor_topic: publish")
        Events.publish("mysignal", True)

        while not ton.q():
            
            print(ton.elapsed_string())
            await asyncio.sleep(delay=0.1)

        print(f"TON IS DONE {ton.elapsed_string()}")

        print("monitor_topic complete")        


    async def test_structured_text():
        """In this test, we test the usage of the start() method, analogous
        to how our programmatic Ton would be used in Structured Text.
        """

        print( "\n\n\nTest structured_text...")

        ton = Ton()
        ton.preset_ms = 3000
        ton.start()


        while not ton.q():

            print(ton.elapsed_string())
            await asyncio.sleep(delay=0.1)

        print(f"TON IS DONE {ton.elapsed_string()}")

        print ("stuctured_text complete")


    async def run_tests():
        """Run all tests in an async method.
        """

        print( "\n\n\nStart running tests...")

        await test_basic()
        await test_monitor()
        await test_structured_text()

        print( "Tests complete")





    try:

        asyncio.run_coroutine_threadsafe(run_tests(), loop)

        print( "Press CTRL-C to stop.")  

        loop.run_forever()

    except KeyboardInterrupt:
        
        print( "Closing from keyboard request.")  


    except Exception as ex:

        print( f"CoreLink exception: {ex}")  
        print(ex)
            
    finally:
        
        loop.stop()

        print( "Goodbye.")
            