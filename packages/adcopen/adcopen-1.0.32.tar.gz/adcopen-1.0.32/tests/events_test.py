'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Friday, 30th April 2021 8:49:25 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)
'''

import logging
import asyncio
import time

from adcopen.events import Events



if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")

    @Events.subscribe("testsig")
    async def testsig_decorator(data):
        print(f"\t\tDecorator Test signal received! {data}")

    async def testsig_method(data):
        print(f"\t\tMethod test signal received! {data}")

    async def later_method(data):
        print(f"\t\tLater method test signal received! {data}")

    async def method_with_topic(topic, data):
        print(f"\t\tMethod with topic {topic} received! {data}")        

    async def test_basic():

        print("Test signal to multiple methods.")
        Events.subscribe_method("testsig", testsig_method)

        await asyncio.sleep(delay=0.5)

        Events.publish("testsig", "First")

        await asyncio.sleep(delay=0.5)

        print("Test removing method.")
        Events.unsubscribe_method("testsig", testsig_method)
        Events.publish("testsig", "Second")

    async def test_onchange():

        print("Test OnChange.\n------------------\n")

        Events.subscribe_method("testsig", testsig_method)

        await asyncio.sleep(delay=0.25)

        # The first event should be posted.
        print("An event should be received by the two listeners....")
        Events.publish("testsig", "Third")

        print("I will now publish the same value again...")

        for x in range(0, 3):
            print("Publishing... (should not see event)")
            await asyncio.sleep(delay=1)
            Events.publish("testsig", "Third")

        await asyncio.sleep(delay=1)

        print("I will now publish a new value. It should be received.")

        Events.publish("testsig", "Fourth")

        await asyncio.sleep(delay=1)
        print("I will now subscribe a new method to the topic. It should get the last value published.")

        Events.subscribe_method("testsig", later_method)

        await asyncio.sleep(delay=1)

        print("I will now publish a repeat value. It should not be received.")

        Events.publish("testsig", "Fourth")

        await asyncio.sleep(delay=1)

        print("I will now publish a new value. It should be received.")
        Events.publish("testsig", "Fifth")

        await asyncio.sleep(delay=1)

        print("test_onchange complete")

    async def test_include_topic():

        print("I will now subscribe a method with a topic parameter... ")
        Events.subscribe_method("meth_topic", method_with_topic, include_topic=True)

        await asyncio.sleep(delay=1)

        print("I will now publish a value on that topic. Both the topic name value should appear.")

        Events.publish("meth_topic", "Gyro")

        await asyncio.sleep(delay=2)

        print("test_include_topic complete")


    async def run_tests():

        await test_basic()
        await test_onchange()

        await test_include_topic()

        print("\n\n--- All done. ---")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:

        asyncio.run_coroutine_threadsafe(run_tests(), loop)

        print("Press CTRL-C to stop.")

        loop.run_forever()

    except KeyboardInterrupt:

        print("Closing from keyboard request.")

    except Exception as ex:

        print(f"Exception: {ex}")

    finally:

        loop.stop()

        print("Goodbye.")
