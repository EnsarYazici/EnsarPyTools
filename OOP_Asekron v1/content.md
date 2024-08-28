
```py
# main.py

import asyncio
import Workers
# async def main():
#     obj1 = Object1()
#     obj2 = Object2()

#     await asyncio.gather(
#         obj1.start(),
#         obj2.start()
#     )
async def main():
    Workers.CreateWorker(3)

    await asyncio.gather(*(obj.run() for obj in Workers.wrks))
if __name__ == "__main__":
    try:
     asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated...")
```
```py
# Object.py

import asyncio

class ObjectBase:
    def __init__(self,id = -1, update_interval=1.0):
        self.update_interval = update_interval
        self.running = True
        self.id = id

    async def run(self):
        await self.start()
        if hasattr(self, 'update'):
            while self.running:
                await self.update()
                await asyncio.sleep(self.update_interval)

    async def start(self):
        pass  # Subclasses can override this method

    def stop(self):
        self.running = False
        print(f"Object{self.id} stopped.")
```
```py
# object1.py ( The for loop is there for testing, it simulates the object having a job with a loop inside itself. So it doesn't have to be in the default code block. )

from Object import ObjectBase
import asyncio
class Object1(ObjectBase):
    def __init__(self,id = -1,update_interval = 1):
        super().__init__(update_interval)
        self.id = id
        self.a = 0
    async def start(self):
        print(f"Object{self.id} start")

    async def update(self):
        print(f"Object{self.id} update")
        for i in range(5):
            print(f"Object{self.id} processing {i}")
            await asyncio.sleep(1)  # Simulate a long-running task
            self.a += 1
        if self.a >= 10:
          self.stop()
```
```py
# Workers.py ( This is there to make it easier to create and test more than one object. So it doesn't have to be in the default code block. )

wrks = []
def CreateWorker(size):
    import object1
    for i in range(size):
        worker = object1.Object1(id=i)
        wrks.append(worker)
```
