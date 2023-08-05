
from adcopen import Events

import asyncio


from adcopen import sae_butterworth



class TestClass(object):

    def __init__(self):
        Events.subscribe_method("evtest",self.myInternal)

    async def myInternal(self, data):
        print(f"Internal callback:{data}")







@Events.subscribe("evtest")
def myExternal(data):
    print(f"External callback:{data}")


tc = TestClass()


try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

Events.publish("evtest", "The quick brown fox yada yada yada.")


try:

    loop.run_forever()  
        
except KeyboardInterrupt:
    
    print( "Closing from keyboard request.")  




