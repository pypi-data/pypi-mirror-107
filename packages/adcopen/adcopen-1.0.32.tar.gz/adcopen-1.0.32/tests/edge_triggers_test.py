'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Friday, 30th April 2021 8:47:58 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''


import asyncio
import logging

from adcopen.events import Events
from adcopen.edge_triggers import RTrig, FTrig


if __name__ == '__main__':


    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")

    @Events.subscribe("rt-done")
    async def rtdone(value):
        print(f"rt-done {value}")

    @Events.subscribe("ft-done")
    async def ftdone(value):
        print(f"ft-done {value}")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def test_basic():
        """Basic test using the RTrig in a non-blocking scenario,
        similar to structured text.
        """

        print("\n\n\nTest basic usage...")

        rt = RTrig(signal="rt-done", userdata="basic usage")
        ft = FTrig(signal="ft-done", userdata="basic usage")

        for x in range(1, 10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        rt.input = True
        ft.input = True

        for x in range(1, 10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        rt.input = False
        ft.input = False

        for x in range(1, 10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        print("Basic usage test complete.")

    async def test_monitor():
        """In this test, the RTrig isn't updated from code, but by
        using asynchronous events.
        """

        print("\n\n\nTest monitor_topic...")

        rt = RTrig(signal="rt-done", userdata="monitor usage",
                   monitor_topic="mysignal")
        ft = FTrig(signal="ft-done", userdata="monitor usage",
                   monitor_topic="mysignal")

        await asyncio.sleep(delay=1)

        print("monitor_topic: publish")
        Events.publish("mysignal", True)

        await asyncio.sleep(delay=3)

        for x in range(1, 10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        Events.publish("mysignal", False)

        for x in range(1, 10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        Events.publish("mysignal", True)

        for x in range(1, 10):

            print(f"rt state: {rt.q()} ft state {ft.q()}")
            await asyncio.sleep(delay=0.1)

        print("monitor_topic test complete")

    async def run_tests():
        """Run all tests in an async method.
        """

        print("\n\n\nStart running tests...")

        await test_basic()
        await test_monitor()

        print("Tests complete")

    try:

        asyncio.run_coroutine_threadsafe(run_tests(), loop)

        print("Press CTRL-C to stop.")

        loop.run_forever()

    except KeyboardInterrupt:

        print("Closing from keyboard request.")

    except Exception as ex:

        print(f"CoreLink exception: {ex}")
        print(ex)

    finally:

        loop.stop()

        print("Goodbye.")
